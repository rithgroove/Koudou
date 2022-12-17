import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__, path='/comparison_infection')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Facts", className="card-text"),

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
        dbc.Tab(tab1_content, label="Facts"),
        dbc.Tab(tab2_content, label="Infection Rate"),
        dbc.Tab(tab3_content, label="Infection for Agent"),
        dbc.Tab(
            "This tab's content is never seen", label="To be develop", disabled=True
        ),
    ], style={'marginTop': '5px'}
)

layout = html.Div(style=style_data_align_0, children=[
        html.Div(
            children=[
                html.H3("Model Comparison for Infection Part", style=style_select_case),
                tabs
            ]
        ),

    ]
)

