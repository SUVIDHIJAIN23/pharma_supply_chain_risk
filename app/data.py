import pandas as pd
import numpy as np
import requests
import math
import os
from joblib import Memory

# ── Constants ──────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'shortage_clean.csv')
CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'cache', 'features')

# ── Fetching ────────────────────────────────────────────────
memory = Memory(CACHE_PATH, verbose=0)
@memory.cache
def get_FDA_data(endpoint, limit=1000):
    """
    Fetches data from the FDA API for a specified endpoint and limit.
    Input:
    - endpoint: FDA API endpoint (e.g., 'shortages.json')
    - limit: max records per request (default 1000)
    Output: list of records
    """
    all_records = []
    skip = 0
    num_records = 0

    while True:
        api_url = f"https://api.fda.gov/drug/{endpoint}?limit={limit}&skip={skip}"
        response = requests.get(api_url)

        if response.status_code == 200:
            try:
                data = response.json()
                if skip == 0:
                    num_records = data.get('meta', {}).get('results', {}).get('total', 0)
                    print(f"Total records available: {num_records}")
                    print(f"Queries needed: {math.ceil(num_records / limit)}")
                records = data.get('results', [])
                all_records.extend(records)
                print(f"Fetched {skip + 1} to {skip + len(records)} of {num_records}")
            except ValueError:
                print("Error: Response is not valid JSON.")
        else:
            print("Please check your endpoint and try again.")

        skip += limit
        if skip >= num_records:
            break

    return all_records


# ── Cleaning ────────────────────────────────────────────────
def update_shortage_reason(row):
    """Fills null shortage_reason based on availability status."""
    if pd.isnull(row['shortage_reason']):
        mapping = {
            'Available': 'Available',
            'To Be Discontinued': 'Not Applicable',
            'Resolved': 'Not Applicable',
            'Unavailable': 'Unavailable',
            'Information pending': 'Information pending'
        }
        row['shortage_reason'] = mapping.get(row['availability'], row['shortage_reason'])
    return row


def clean_data(df):
    """Applies all cleaning steps to raw DataFrame. Returns cleaned DataFrame."""

    # Extract from nested openfda column
    df['brand_name'] = df['openfda'].apply(
        lambda x: x.get('brand_name', [None])[0] if isinstance(x, dict) else None)
    df['route'] = df['openfda'].apply(
        lambda x: ", ".join(y for y in x.get('route', []) if y) if isinstance(x, dict) else None)

    # Parse dates
    for col in ['initial_posting_date', 'update_date', 'discontinued_date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Extract first therapeutic category
    df['therapeutic_category'] = df['therapeutic_category'].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)

    # Fix availability typos
    df['availability'] = df['availability'].str.strip().replace({
        'Limited Availabiltiy': 'Limited Availability',
        'Limited Availablity': 'Limited Availability'
    })

    # Fill null availability from status
    df.loc[df['availability'].isna() & (df['status'] == 'Resolved'), 'availability'] = 'Resolved'
    df.loc[df['availability'].isna() & (df['status'] == 'To Be Discontinued'), 'availability'] = 'To Be Discontinued'

    # Fill null shortage_reason
    df = df.apply(update_shortage_reason, axis=1)

    # Feature engineering
    df['year'] = df['initial_posting_date'].dt.year
    df['duration_days'] = (df['update_date'] - df['initial_posting_date']).dt.days

    # Drop irrelevant columns
    df.drop(columns=[
        'package_ndc', 'contact_info', 'related_info', 'presentation',
        'change_date', 'resolved_note', 'related_info_link', 'openfda'
    ], inplace=True)

    return df


# ── Load Data ───────────────────────────────────────────────
def load_data():
    """
    Loads cleaned data from CSV if available.
    Falls back to FDA API fetch + clean if CSV not found.
    Returns cleaned DataFrame and categorical columns list.
    """
    if os.path.exists(DATA_PATH):
        print(f"Loading data from {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
        for col in ['initial_posting_date', 'update_date', 'discontinued_date']:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    else:
        print("CSV not found — fetching from FDA API...")
        records = get_FDA_data('shortages.json', limit=1000)
        df = pd.DataFrame(records)
        df = clean_data(df)
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
        print(f"Saved clean data to {DATA_PATH}")

    categorical_columns = [
        'availability', 'therapeutic_category',
        'dosage_form', 'company_name', 'brand_name'
    ]

    return df, categorical_columns