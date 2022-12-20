import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *

dash.register_page(__name__)

layout = html.Div(style=style_title,
    children=[
        html.H2(children="Evacuation Analysis"),
        html.Div([
            html.Div(style=style_title, children=[
                html.Label('Agent ID  '),
                dcc.Input(value='1', type='text'),
                html.Br(),
                html.Br(),
                html.Label('Variables'),
                dcc.Dropdown(['agent_location', 'agent_state', 'agent_profession',
                              'activity', 'infection_type', 'node_id',
                              'household_id'],
                             ['agent_location', 'agent_state', 'agent_profession'],
                             multi=True),
            ]),
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        dbc.InputGroup(
            [
                dbc.Button("Random name", id="input-group-button", n_clicks=0),
                dbc.Input(id="input-group-button-input", placeholder="name"),
            ]
        )
    ]
)


@callback(
    Output("input-group-button-input", "value"),
    [Input("input-group-button", "n_clicks")],
)
def on_button_click(n_clicks):
    if n_clicks:
        names = ["Arthur Dent", "Ford Prefect", "Trillian Astra"]
        which = n_clicks % len(names)
        return names[which]
    else:
        return ""
