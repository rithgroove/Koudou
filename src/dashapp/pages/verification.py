import dash
from .public.utils import *
from dash import dcc, html, callback, State, Input, Output
from .public.css import *
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div([
    html.Div(style=style_offcanvas, children=[
            dbc.Button("Instructions", id="open-offcanvas", n_clicks=0),
            dbc.Offcanvas(
                html.P(
                    "We are going to test several scenarios that would give bias and failure to the simulation model."
                    " There is a google doc plugged in which you can write more test requirement ideas."
                ),
                id="offcanvas",
                title="How Verification Works",
                is_open=False,
            ),
        ]),
])


