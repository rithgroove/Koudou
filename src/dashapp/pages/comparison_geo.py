import dash
import numpy
import pandas
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *
import plotly.express as px
from .public.utils import *
from .public.File_Factory import *

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
                        text_color="warning",
                        className="border me-1",
                        style=style_fontSize20
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                className='container-fluid',
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model One"),
                                html.Div(id='count-proportion-pie-model-one'),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Two"),
                                html.Div(id='count-proportion-pie-model-two'),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Three"),
                                html.Div(id='count-proportion-pie-model-three'),
                            ])
                        ]
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
                        text_color="warning",
                        className="border me-1",
                        style=style_fontSize20
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                className='container-fluid',
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model One", id="random-input-model-one"),
                                html.Div(id='count-proportion-table-model-one'),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Two", id="random-input-model-two"),
                                html.Div(id='count-proportion-table-model-two'),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Three", id="random-input-model-three"),
                                html.Div(id='count-proportion-table-model-three'),
                            ])
                        ]
                    ),
                ]
            ),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Agent Location Proportion Summary"),
        # dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            "This tab's content is never seen", label="To be developed", disabled=True
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
])


@callback(
    Output('count-proportion-pie-model-one', 'children'),
    Input('random-input-model-one', 'value')
)
def pie_return_model_one(value):
    f = ModelOne()
    df_agent_position_summary = f.agent_position_summary
    counts_dict = proportion_calculation(df_agent_position_summary)
    fig = pie_return_html(counts_dict)

    if df_agent_position_summary is pandas.NA:
        return html.H5("Not loaded yet, please upload agent_position_summary.csv to model one.")
    else:
        return dcc.Graph(figure=fig)


@callback(
    Output('count-proportion-pie-model-two', 'children'),
    Input('random-input-model-two', 'value')
)
def pie_return_model_two(value):
    f = ModelTwo()
    df_agent_position_summary = f.agent_position_summary
    counts_dict = proportion_calculation(df_agent_position_summary)
    fig = pie_return_html(counts_dict)

    if df_agent_position_summary is pandas.NA:
        return html.H5("Not loaded yet, please upload agent_position_summary.csv to model one.")
    else:
        return dcc.Graph(figure=fig)


@callback(
    Output('count-proportion-pie-model-three', 'children'),
    Input('random-input-model-three', 'value')
)
def pie_return_model_three(value):
    f = ModelThree()
    df_agent_position_summary = f.agent_position_summary
    counts_dict = proportion_calculation(df_agent_position_summary)
    fig = pie_return_html(counts_dict)

    if df_agent_position_summary is pandas.NA:
        return html.H5("Not loaded yet, please upload agent_position_summary.csv to model one.")
    else:
        return dcc.Graph(figure=fig)


@callback(
    Output('count-proportion-table-model-one', 'children'),
    Input('random-input-model-one', 'value')
)
def table_return_model_one(value):
    f = ModelOne()
    df_agent_position_summary = f.agent_position_summary
    counts_dict = proportion_calculation(df_agent_position_summary)

    fig = table_return_html(counts_dict)
    if df_agent_position_summary is pandas.NA:
        return html.H5("Not loaded yet, please upload agent_position_summary.csv to model one.")
    else:
        return dcc.Graph(figure=fig)


@callback(
    Output('count-proportion-table-model-two', 'children'),
    Input('random-input-model-two', 'value')
)
def table_return_model_one(value):
    f = ModelTwo()
    df_agent_position_summary = f.agent_position_summary
    counts_dict = proportion_calculation(df_agent_position_summary)

    fig = table_return_html(counts_dict)
    if df_agent_position_summary is pandas.NA:
        return html.H5("Not loaded yet, please upload agent_position_summary.csv to model two.")
    else:
        return dcc.Graph(figure=fig)


@callback(
    Output('count-proportion-table-model-three', 'children'),
    Input('random-input-model-three', 'value')
)
def table_return_model_three(value):
    f = ModelThree()
    df_agent_position_summary = f.agent_position_summary
    counts_dict = proportion_calculation(df_agent_position_summary)

    fig = table_return_html(counts_dict)
    if df_agent_position_summary is pandas.NA:
        return html.H5("Not loaded yet, please upload agent_position_summary.csv to model three.")
    else:
        return dcc.Graph(figure=fig)
