from app import app
from dash import Dash, dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc


#Initializing categorical columns
categorical_columns = [
        'availability', 'therapeutic_category',
        'dosage_form', 'company_name', 'brand_name'
    ]

app.layout = dbc.Container([
    html.H2("Pharmaceutical Drug Shortage Analysis", className="card-title px-2 py-2 pt-2"),
    
    # Row 1 — Introduction
    dbc.Row([
        dbc.Col([
            html.H4("An Interactive Tutorial Using Plotly Dash and Dash Bootstrap Components", className="card-title px-2"),
            html.P("Drug shortages are not random events — they follow structural patterns \
                    tied to manufacturing concentration, regulatory failures, and demand volatility.",
                    className="px-2 mb-1"),
            html.P([
                "Data sourced from the OpenFDA public API. ",
                html.A("OpenFDA Drug Shortages",
                        href="https://open.fda.gov/apis/drug/drugshortages/",
                        target="_blank"),
                " — 1,686 records spanning 2012 to 2026."
            ], className="px-2 mb-1 text-muted"),
        ])
    ]),
    html.Br(),

    # Row 2 — Filters
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Filters"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Date Range to filter:"),
                            dcc.DatePickerRange(
                                id="dr",
                                start_date="2015-01-01",
                                end_date="2026-02-01"
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Categories to filter:"),
                            dcc.Dropdown(
                                id="categorial_dd",
                                options=[{"label": c, "value": c} for c in categorical_columns],
                                value="therapeutic_category"
                            )
                        ], width=6)
                    ])
                ])
            ])
        )
    ]),
    html.Br(),

    # Row 3 — Line chart + Bar chart
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Drug Shortage Trends Over Time"),
                html.P("Tracks the number of drug shortages first posted per year. \
                        Shortages have structurally increased since 2012, with notable spikes \
                        in 2023 reflecting post-COVID supply stress, and 2025 dominated by \
                        manufacturer discontinuation announcements rather than new shortages.",
                        className="px-3 py-2 text-muted"),
                dcc.Graph(id="timeseries-shortagecount-chart")
            ])
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Shortage Count by Selected Category"),
                html.P("Compares shortage counts across the selected categorical dimension. \
                        Use the dropdown above to switch between therapeutic categories, \
                        manufacturers, dosage forms, and brand names — revealing where \
                        supply concentration risk is highest.",
                        className="px-3 py-2 text-muted"),
                dcc.Graph(id="barchart-shortagecount-categorical-chart")
            ])
        ], width=6),
    ]),
    html.Br(),

    # Row 4 — Shortage reasons + Box plot
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Primary Reasons for Drug Shortages"),
                html.P("Breaks down the root causes of shortages among drugs that are \
                        currently unavailable or limited. 34% of shortages have no disclosed \
                        cause — a transparency gap in itself. Among identified causes, \
                        active ingredient shortages and demand surges account for nearly \
                        half of all cases.",
                        className="px-3 py-2 text-muted"),
                dcc.Graph(id="shortagereason-barchart")
            ])
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Shortage Duration Distribution by Category"),
                html.P("Shows the distribution of shortage duration in days across the \
                        selected categorical dimension, filtered to drugs that are currently \
                        unavailable or resolved — where duration is most reliable. \
                        Wider boxes indicate higher variability in how long shortages persist.",
                        className="px-3 py-2 text-muted"),
                dcc.Graph(id="boxplot-unavailableduration-distribution-chart")
            ])
        ], width=6),
    ]),
    html.Br(),

    # Row 5 — Scatter plot
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Risk Quadrant: Shortage Frequency vs. Median Duration"),
                html.P("Each point represents an entity in the selected category — plotted \
                        by number of shortages (x-axis) against median shortage duration in \
                        days (y-axis). Entities in the upper-right quadrant are both \
                        high-frequency and long-duration — representing the highest structural \
                        supply chain risk.",
                        className="px-3 py-2 text-muted"),
                dcc.Graph(id="scatter_plot_durationvsshortage")
            ])
        ], width=12)
    ])

    ], fluid=True)