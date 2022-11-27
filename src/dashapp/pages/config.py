import dash
from dash import html, dash_table, callback, dcc, Input, Output
from .public.css import *
from .public.data import *

dash.register_page(__name__)

layout = html.Div(children=[
    html.Span('Basic Simulation Params', className="badge bg-dark", style=style_badge),
    html.Div(style=style_data_table, children=[
        dash_table.DataTable(
            data=default_config_df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in default_config_df.columns],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in default_config_df.to_dict('records')
            ],
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            tooltip_delay=0,
            tooltip_duration=None
        ),
    ]),
    html.Br(),
    html.Span('Params by Category', className="badge bg-dark", style=style_badge),
    html.Div([
        html.Div(style=style_files_show_div, children=[
            html.Label('SIM_CONFIG'),
            html.Div(style=style_dropdown, children=[
                dcc.Dropdown(['condition', 'attributes.basic',
                              'attributes.option', 'attributes.updateable',
                              'attributes.schedule', 'attributes.profession',
                              'behaviors.normal', 'behaviors.evacuate',
                              'behaviors.self_isolation', 'behaviors.severe',
                              ],
                             'condition',
                             id="file-name")
            ]),
            html.Div(id="location-text")
        ]),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Div(
        style=style_configs_div, children=[

        ]
    )
])

@callback(
    Output("location-text", "children"),
    Input("file-name", "value"))
def return_location(file_name):
    addr_list = file_name.split(".")
    if len(addr_list) == 1:
        return [html.Div("File location: " + str(defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0])))]
    else:
        return [html.Div("File location: " + str(defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0]).get(addr_list[1])))]
