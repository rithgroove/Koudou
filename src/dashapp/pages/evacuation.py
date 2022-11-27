import dash
from dash import html, dcc, callback, Input, Output
from .public.css import *

dash.register_page(__name__)

layout = html.Div(style=style_title,
    children=[
        html.H2(children="Evacuation Analytics"),
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
        ], style={'display': 'flex', 'flex-direction': 'row'})
    ]
)