import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__, path='/comparison_log')


log_data_lines = []
html_list1 = []
for i in range(len(log_data_lines)):
    html_list1.append(html.H5(log_data_lines[i]))

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                children=[
                    html.Span('Simulation Log for Model 1', className="badge bg-dark", style=style_badge1),
                    html.Div(style=style_log, children=html_list1)
                ]
            ),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                children=[
                    html.Span('Simulation Log for Model 2', className="badge bg-dark", style=style_badge1),
                    html.Div(style=style_log, children=html_list1)
                ]
            ),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                children=[
                    html.Span('Simulation Log for Model 3', className="badge bg-dark", style=style_badge1),
                    html.Div(style=style_log, children=html_list1)
                ]
            ),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Log info from Model 1"),
        dbc.Tab(tab2_content, label="Log Info from Model 2"),
        dbc.Tab(tab3_content, label="Log Info from Model 3")
    ], style={'marginTop': '5px'}
)

layout = html.Div(style=style_data_align_0, children=[
        html.Div(
            children=[
                html.H3("Model Comparison for Logging Part", style=style_select_case),
                tabs
            ]
        ),

    ]
)
