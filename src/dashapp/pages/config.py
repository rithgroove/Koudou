import os
import dash
from dash import callback, dcc, Input, Output, State
from .public.css import *
from .public.data import *
from .public.utils import *
import dash_bootstrap_components as dbc
import pandas as pd

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
            html.Label('Configuration Locations'),
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
            html.Div(
                [
                    dbc.Button("Tips", id="open-lg", className="me-1", outline=True, color='info', n_clicks=0),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Tip")),
                            dbc.ModalBody("All detailed configuration files are categorized in the file parameters/deafult.py."
                                          " Based on file types, the dropdown bar will show all the parameter files by "
                                          "categorization."),
                        ],
                        id="modal-lg",
                        size="lg",
                        is_open=False,
                    ),
                ], style=style_tips
            ),
        ]),
    ]),
    html.Div(
        style=style_configs_div, children=[
            html.Div(id='tables')
        ]
    )
])

callback(
    Output("modal-lg", "is_open"),
    Input("open-lg", "n_clicks"),
    State("modal-lg", "is_open"),
)(toggle_modal)


@callback(
    Output("location-text", "children"),
    Input("file-name", "value"))
def return_location(file_name):
    addr_list = file_name.split(".")
    if len(addr_list) == 1:
        return [html.Div("File location: " + str(defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0])))]
    else:
        return [html.Div("File location: " + str(defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0]).get(addr_list[1])))]

@callback(
    Output('tables', "children"),
    Input("file-name", "value"))
def return_tables(file_name):
    addr_list = file_name.split(".")
    if len(addr_list) == 1:
        file_list = defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0])
    elif len(addr_list) == 2:
        file_list = defaultParam.parameters.get("SIM_CONFIG").get(addr_list[0]).get(addr_list[1])

    path_list = []
    if isinstance(file_list, list):
        for item in file_list:
            path_list.append(os.path.abspath(os.path.join(os.getcwd(), "../.."))+"/"+item)
    else:
        path_list.append(os.path.abspath(os.path.join(os.getcwd(), "../..")) + "/" + file_list)

    html_table_list = []
    for i in range(len(path_list)):
        fig = table_generator(pd.read_csv(path_list[i]))
        fig.update_layout(
            plot_bgcolor='#E6E6FA',  # 图的背景颜色
            paper_bgcolor='#F8F8FF',  # 图像的背景颜色
            height=300,
            # width=1000,
            showlegend=False,
            margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
        )
        if isinstance(file_list, list):
            html_table_list.append(html.Span(file_list[i], className="badge bg-light", style=style_badge_table))
        else:
            html_table_list.append(html.Span(file_list, className="badge bg-light", style=style_badge_table))
        html_table_list.append(dcc.Graph(figure=fig))

    return html_table_list
