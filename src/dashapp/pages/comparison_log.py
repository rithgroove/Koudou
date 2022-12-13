import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__, path='/comparison_log')


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 3!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
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
