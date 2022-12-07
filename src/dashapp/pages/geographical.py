import dash
from dash import html, dcc, Input, Output, callback
from .public.css import *
from .public.utils import location_divider
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
import os

dash.register_page(__name__)

df_agent_position_summary = pd.read_csv(os.getcwd() + './data/simulation_result/agent_position_summary.csv')
location_list = df_agent_position_summary['location'].unique()


layout = html.Div(style=style_title,
    children=[
        html.Span('Agent Location Analysis', className="badge bg-dark", style=style_badge),
        html.Div(style=style_data_align_0, children=[
            html.H4("All locations are listed: "),
            html.H4(location_list + ' ')

        ])
    ]
)

# @callback(
#     Output("location-time-series-chart", "figure"),
#     Input("ticker", "value"))
# def display_time_series(ticker):
#
#     fig = px.line(f.infection_summary, x='time_stamp', y=ticker)
#     fig.update_layout(
#         plot_bgcolor='#E6E6FA',  # 图的背景颜色
#         # paper_bgcolor='#F8F8FF',  # 图像的背景颜色
#         height=400,
#         width=600,
#         showlegend=False,
#         margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
#     )
#     return fig