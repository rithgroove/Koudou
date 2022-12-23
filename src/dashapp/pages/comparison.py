import dash
from dash import html
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__, path='/comparison_intro')

card_infection = dbc.Card([
    # dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
    dbc.CardBody(
        [
            html.H4("Infection Comparison", className="card-title"),
            html.P(
                "Some quick example text to build on the card title and "
                "make up the bulk of the card's content.",
                className="card-text",
            ),
            dbc.Button("Go there", color="primary", href='/comparison_infection'),
        ]
    ),
],
    style={"width": "99%"},
)

card_evacuation = dbc.Card([
    # dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
    dbc.CardBody(
        [
            html.H4("Evacuation Comparison", className="card-title"),
            html.P(
                "Some quick example text to build on the card title and "
                "make up the bulk of the card's content.",
                className="card-text",
            ),
            dbc.Button("Go there", color="primary", href='/comparison_evacuation'),
        ]
    ),
],
    style={"width": "99%"},
)

card_location = dbc.Card([
    # dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
    dbc.CardBody(
        [
            html.H4("Location Comparison", className="card-title"),
            html.P(
                "Some quick example text to build on the card title and "
                "Some quick example text to build on the card title and "
                "Some quick example text to build on the card title and "
                "Some quick example text to build on the card title and "
                "Some quick example text to build on the card title and "
                "Some quick example text to build on the card title and "
                "make up the bulk of the card's content.",
                className="card-text",
            ),
            dbc.Button("Go there", color="primary", href='/comparison_geo'),
        ]
    ),
],
    style={"width": "99%"},
)

layout = html.Div(style={'marginTop': '5px'}, children=[
    html.Div(
        style={}, children=[
            html.Span('Model Comparison', className="badge bg-dark", style=style_badge),
        ]
    ),
    html.Div(className="container", children=[
        html.Div(className="row", children=[
            html.Div(className="col-sm", children=[
                card_infection
            ]),
            html.Div(className="col-sm", children=[
                card_evacuation
            ]),
            html.Div(className="col-sm", children=[
                card_location
            ])
        ])
    ]),
])
