import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__, path='/comparison_geo')


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Comparison based on agent position summary", className="card-text"),
            dbc.Button("Link to there", color="success", href='/geographical'),
            html.Hr(),
            html.Div(
                style=style_data_align_4,
                children=[
                    dbc.Badge(
                        "Pie Charts",
                        color="white",
                        text_color="secondary",
                        className="border me-1",
                    ),
                ]
            ),
            html.Hr(),
            html.Div(
                style=style_data_align_4,
                children=[
                    dbc.Badge(
                        "Tables",
                        color="white",
                        text_color="secondary",
                        className="border me-1",
                    ),
                ]
            )
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Agent Location Proportion Summary"),
        # dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            "This tab's content is never seen", label="To be develop", disabled=True
        ),
    ], style={'marginTop': '5px'}
)

layout = html.Div(style=style_data_align_0, children=[
        html.Div(
            children=[
                html.H3("Model Comparison for Location Part", style=style_select_case),
                tabs
            ]
        ),

    ]
)
