import pandas as pd
import numpy as np
import plotly.express as px


# Helper Function to filter by date:
def filter_by_date_range(df,start_date, end_date):
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    df_filtered = df[
        (df['initial_posting_date'] >= start) &
        (df['initial_posting_date'] <= end)
    ]
    return df_filtered

# Helper Function 1: Temporal Trend
def make_plot_temporal_trends(df_filtered):
    '''
    Plots temporal trends of shortage over years.
    Input - Filtered dataframe
    Output - Plotly figure
    '''
    yearly = df_filtered.groupby('year').size().reset_index(name='count')
    fig = px.line(yearly, x='year', y='count', markers=True)
    # Update y label:
    fig.update_layout(yaxis_title='Drug Shortage Count')
    # Updating the theme
    fig.update_layout(template='ggplot2')
    return fig


# Helper Function 2: Bar chart
def make_bar_chart_categorical(df_filtered,groupby_category):
    '''
    Plots vertical bar chart for categorical variables like therapeutic categories, dose form, etc.
    The plot shows shortage aggregated over filtered time frame for each entity of the selected category (Top 10).
    Input - Filtered dataframe, groupby_category
    Output - Plotly figure
    '''
    category_counts = df_filtered[groupby_category].value_counts().reset_index().sort_values('count', ascending=False).head(10)
    category_counts.columns = [groupby_category, 'count']
    fig = px.bar(category_counts, x=groupby_category, y='count',
                 labels={groupby_category: groupby_category.capitalize(), 'count': 'Shortage Count'})
    fig.update_layout(yaxis_title='Drug Shortage Count')
    # Updating the theme
    fig.update_layout(template='ggplot2')
    return fig


# Helper Function 3: Horizontal Bar Chart
def make_hbar_shortageReason_distribution(df_filtered):
    '''
    Plots horizontal bar chart for shortage reasons (Top 5)
    Input - Filtered dataframe
    Output - Plotly figure
    '''
    df_filtered = df_filtered[(df_filtered['availability'] != 'Available') & (df_filtered['shortage_reason'] !='Not Applicable')]  # Filter to only include unavailable drugs
    shortage_counts = df_filtered.groupby('shortage_reason').size().reset_index(name='count').sort_values('count', ascending=False)
    shortage_counts = shortage_counts[shortage_counts['count'] > np.median(shortage_counts['count'])].head(5)
    fig = px.bar(shortage_counts,
             x='count',
             y='shortage_reason',
             orientation='h',
             labels={'shortage_reason': 'shortage_reason', 'count': 'Number of Shortages'})
    fig.update_layout(xaxis_title='Drug Shortage Count')
    # Updating the theme
    fig.update_layout(template='ggplot2')
    return fig


# Helper Function 4: Box Plot
def make_boxplot_unavailable_duration(df_filtered, groupby_category):
    '''
    Plots box plot showing median shortage duration (updated_date - initial_date for unavailable drugs) aggregated by categorical variables like therapeutic categories, dose form, etc.
    The plot shows shortage aggregated over filtered time frame for each entity of the selected category (Top 10).
    Input - Filtered dataframe, groupby_category
    Output - Plotly figure
    '''
    # data is filtered for availability status as 'Unavailable', and 'Resolved' - just to see the impacted drugs
    # Excluding 'To Be Discontinued' (permanent exits, not shortages) and zero-duration records (same-day FDA entries with no monitoring period)
    # Keeping 'Resolved' as historical benchmark for completed shortage duration;

    reliable_states = ['Unavailable', 'Resolved']
    df_duration = df_filtered[
        (df_filtered['duration_days'] > 0) &
        (df_filtered['availability'].isin(reliable_states))
    ]
    top_categories = (df_duration.groupby(groupby_category)['duration_days'].median() .sort_values(ascending=False).head(10).index.tolist())
    df_duration = df_duration[df_duration[groupby_category].isin(top_categories)]
    df_duration = df_duration.sort_values('duration_days', ascending=False)
    fig = px.box(df_duration, x=groupby_category, y='duration_days')
    fig.update_layout(yaxis_title='Median Shortage Duration (in days)')
    # Updating the theme
    fig.update_layout(template='ggplot2')
    return fig


# Helper Function 5: Scatter plot of median shortage duration v/s drug shortage count for a given categorical variable (like therapeutic_category)
def make_scatter_plot_durationvsshortage(df_filtered, groupby_category):
  '''
  Plots scatter plot of median shortage duration v/s drug shortage count for a given categorical variable (like therapeutic_category)
  Size of the point is proportional to the count of drug shortages (Top 10 entities are shown on the plot)
  The plot shows shortage aggregated over filtered time frame for each entity of the selected category.
  Input - Filtered dataframe, groupby_category
  Output - Plotly figure
  '''

  # data is filtered for availability status as 'Unavailable', and 'Resolved' - just to see the impacted drugs
  # Excluding 'To Be Discontinued' (permanent exits, not shortages) and zero-duration records (same-day FDA entries with no monitoring period)
  # Keeping 'Resolved' as historical benchmark for completed shortage duration;

  reliable_states = ['Unavailable', 'Resolved']
  df_duration = df_filtered[
      (df_filtered['duration_days'] > 0) &
      (df_filtered['availability'].isin(reliable_states))
  ]
  scatter_data = df_duration.groupby(groupby_category).agg(
      shortage_count=('duration_days', 'count'),
      median_duration=('duration_days', 'median')
  ).reset_index().head(10)
  fig = px.scatter(scatter_data,
                  x='shortage_count',
                  y='median_duration',
                  text=groupby_category,
                  size='shortage_count',
                  labels={'shortage_count': 'Number of Shortages',
                          'median_duration': 'Median Duration (days)'})
  fig.update_traces(textposition='top center')
  fig.update_layout(yaxis_title='Median Shortage Duration (in days)')
  fig.update_layout(xaxis_title='Drug Shortage Count')
  # Updating the theme
  fig.update_layout(template='ggplot2')
  return fig


