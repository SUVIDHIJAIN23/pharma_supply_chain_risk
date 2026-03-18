from dash import callback, Input, Output
from figures import (filter_by_date_range, 
                     make_plot_temporal_trends, 
                     make_bar_chart_categorical, 
                     make_hbar_shortageReason_distribution, 
                     make_boxplot_unavailable_duration, 
                     make_scatter_plot_durationvsshortage
                    )
from data import load_data

# Loading Data
df, categorical_columns = load_data()

#Fig 1: Temporal Trend
@callback(
    Output("timeseries-shortagecount-chart", "figure"),
    Input("dr", "start_date"),
    Input("dr","end_date"),
)
def plot_temporal_trends(start_date, end_date):
    df_filtered = filter_by_date_range(df,start_date, end_date)
    return make_plot_temporal_trends(df_filtered)

# Figure 2: Vertical Bar Chart
@callback(
    Output("barchart-shortagecount-categorical-chart", "figure"),
    Input("dr", "start_date"),
    Input("dr","end_date"),
    Input("categorial_dd","value")
)
def bar_chart_categorical(start_date, end_date, groupby_category):
    df_filtered = filter_by_date_range(df,start_date, end_date)
    return make_bar_chart_categorical(df_filtered,groupby_category)

# Fig 3: Horizontal Bar Chart - Reasons for Shortages
@callback(
    Output("shortagereason-barchart", "figure"),
    Input("dr", "start_date"),
    Input("dr","end_date"),
)

# Fig 3: Horizontal Bar Chart — Reasons for Shortages
def hbar_category_distribution(start_date, end_date):
    df_filtered = filter_by_date_range(df,start_date, end_date)
    return make_hbar_shortageReason_distribution(df_filtered)


# Fig 4: Estimating Median Shortage duration for each entity in the categories:
@callback(
    Output("boxplot-unavailableduration-distribution-chart", "figure"),
    Input("dr", "start_date"),
    Input("dr","end_date"),
    Input("categorial_dd","value")
)
def unavailable_duration(start_date, end_date, category):
    df_filtered = filter_by_date_range(df,start_date, end_date)
    return make_boxplot_unavailable_duration(df_filtered,category)


# Fig 5: Scatter plot of median shortage duration v/s drug shortage count for a given categorical variable (like therapeutic_category)
@callback(
    Output("scatter_plot_durationvsshortage", "figure"),
    Input("dr", "start_date"),
    Input("dr","end_date"),
    Input("categorial_dd","value")
)
def scatter_plot_durationvsshortage(start_date, end_date, category):
    df_filtered = filter_by_date_range(df,start_date, end_date)
    return make_scatter_plot_durationvsshortage(df_filtered,category)
