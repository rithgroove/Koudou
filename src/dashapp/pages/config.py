import dash
from dash import html, dash_table, callback, dcc, Input, Output
import parameters.default as defaultParam
from collections import OrderedDict
import pandas as pd

style_title = {
    'textAlign': 'center',
    'marginLeft': '100px',
    'marginRight': '100px',
}

style_dropdown = {
    'width': '250px'
}

data_default_config = OrderedDict(
    [
        (
            "Parameter",
            ["SEED",
             "N_AGENTS",
             "THREADS",
             "GRID_SIZE",
             "STEP_LENGTH",
             "MAX_STEPS",
             "EVACUATION.SHARE_INFO_CHANCE",
             "EVACUATION.DISTANCE",
             ],
        ),
        (
            "Value",
            [str(defaultParam.parameters.get("SEED")),
             str(defaultParam.parameters.get("N_AGENTS")),
             str(defaultParam.parameters.get("THREADS")),
             str(defaultParam.parameters.get("GRID_SIZE")),
             str(defaultParam.parameters.get("STEP_LENGTH")),
             str(defaultParam.parameters.get("MAX_STEPS")),
             str(defaultParam.parameters.get("EVACUATION").get("SHARE_INFO_CHANCE")),
             str(defaultParam.parameters.get("EVACUATION").get("DISTANCE")),
             ],
        ),
        (
            "Description",
            ["Used for reproducing experiments",
             "Number of agents in the simulation",
             "Number of CPUs be used for pathfinding",
             "Used when calculating the centroid for buildings",
             "Each step is one second",
             "This is simulating for 7 weeks",
             "Agents have 80% chance of sharing information",
             "if they have a distance less than 10"
             ]
        ),
    ]
)

default_config_df = pd.DataFrame(data_default_config)

dash.register_page(__name__)

layout = html.Div(style=style_title,
    children=[
        html.H2(children="Configuration Description"),
        html.H3("File Location: parameters/default.py"),
        dash_table.DataTable(
            data=default_config_df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in default_config_df.columns],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in default_config_df.to_dict('records')
            ],

            # Overflow into ellipsis
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            tooltip_delay=0,
            tooltip_duration=None
        ),
        html.Br(),
        html.Br(),
        html.Div([
            html.Div(style=style_dropdown, children=[
                html.Label('SIM_CONFIG'),
                dcc.Dropdown(['condition', 'attributes.basic',
                              'attributes.option', 'attributes.updateable',
                              'attributes.schedule','attributes.profession',
                              'behaviors.normal','behaviors.evacuate',
                              'behaviors.self_isolation','behaviors.severe',
                              ],
                             'condition',
                             id="file-name"),
                html.Br(),
                html.Div(id="location-text")
            ]),
        ], style={'display': 'flex', 'flex-direction': 'row'}),
    ]
)


@callback(
    Output("location-text", "children"),
    Input("file-name", "value"))
def return_location(file_name):
    addr_list = file_name.split(".")
    if len(addr_list) == 1:
        return [
            html.Div("File location: " + str(defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0])))
        ]
    else:
        return [
            html.Div("File location: " + str(defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0]).get(addr_list[1])))
        ]
