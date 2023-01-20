import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__, path='/comparison_evacuation')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        [
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Facts"),
        dbc.Tab(tab2_content, label="Agent Behavior Tracking"),
        dbc.Tab(tab3_content, label="Mask in Evacuation"),
        dbc.Tab(tab4_content, label="Evacuation Location Analysis"),
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