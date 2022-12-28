import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__, path='/comparison_evacuation')

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

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            "To be develop", label="To be develop", disabled=True
        ),
    ], style={'marginTop': '5px'}
)

layout = html.Div(style=style_data_align_0, children=[
        html.Div(
            children=[
                html.H3("Model Comparison for Evacuation Part", style=style_select_case),
                tabs
            ]
        ),

    ]
)