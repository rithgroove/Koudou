import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from .public.css import *
from .public.File_Factory import ModelOne, ModelTwo, ModelThree

dash.register_page(__name__, path='/comparison_log')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                children=[
                    html.Span('Simulation Log for Model 1', className="badge bg-dark",
                              style=style_badge1, id='input_log1'),
                    html.Div(style=style_data_align_1, id='log-model1')
                ]
            ),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                children=[
                    html.Span('Simulation Log for Model 2', className="badge bg-dark",
                              style=style_badge1, id='input_log2'),
                    html.Div(style=style_data_align_1, id='log-model2')
                ]
            ),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                children=[
                    html.Span('Simulation Log for Model 3', className="badge bg-dark",
                              style=style_badge1, id='input_log3'),
                    html.Div(style=style_data_align_1, id='log-model3')
                ]
            ),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Log info from Model 1"),
        dbc.Tab(tab2_content, label="Log Info from Model 2"),
        dbc.Tab(tab3_content, label="Log Info from Model 3")
    ], style={'marginTop': '5px'}
)

layout = html.Div(style=style_data_align_0, children=[
    html.Div(
        children=[
            html.H3("Model Comparison for Logging Part", style=style_select_case),
            tabs
        ]
    ),
])


@callback(
    Output('log-model1', 'children'),
    Input('input_log1', 'value')
)
def display_log_model1(i):
    f = ModelOne()
    return html.Div(children=f.log)


@callback(
    Output('log-model2', 'children'),
    Input('input_log2', 'value')
)
def display_log_model1(i):
    f = ModelTwo()
    return html.Div(children=f.log)


@callback(
    Output('log-model3', 'children'),
    Input('input_log3', 'value')
)
def display_log_model1(i):
    f = ModelThree()
    return html.Div(children=f.log)
