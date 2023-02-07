import random
import dash
from dash import html, dcc, callback, Input, Output, State
from .public.File_Factory import *
from .public.utils_list.comp_infection_util import *

dash.register_page(__name__, path='/comparison_infection')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                className='container-fluid',
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model One", id='facts-input-model-one'),
                                html.Div(id='facts-model-one'),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Two", id='facts-input-model-two'),
                                html.Div(id='facts-model-two'),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Three", id='facts-input-model-three'),
                                html.Div(id='facts-model-three'),
                            ])
                        ]
                    ),
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
                className='container-fluid',
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model One"),
                                dcc.Graph(style=style_title, id="IP1-time-series-chart"),
                                html.Br(),
                                html.P(style=style_title, children="Select Cases"),
                                dcc.Checklist(
                                    style=style_title,
                                    id="IP1-ticker",
                                    options=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe",
                                             "recovered"],
                                    value=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe",
                                           "recovered"],
                                    inline=True
                                ),
                                html.Hr(),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Two"),
                                dcc.Graph(style=style_title, id="IP2-time-series-chart"),
                                html.Br(),
                                html.P(style=style_title, children="Select Cases"),
                                dcc.Checklist(
                                    style=style_title,
                                    id="IP2-ticker",
                                    options=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe",
                                             "recovered"],
                                    value=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe",
                                           "recovered"],
                                    inline=True
                                ),
                                html.Hr(),
                            ]),
                            html.Div(className='col-sm-4', children=[
                                html.H5("Model Three"),
                                dcc.Graph(style=style_title, id="IP3-time-series-chart"),
                                html.Br(),
                                html.P(style=style_title, children="Select Cases"),
                                dcc.Checklist(
                                    style=style_title,
                                    id="IP3-ticker",
                                    options=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe",
                                             "recovered"],
                                    value=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe",
                                           "recovered"],
                                    inline=True
                                ),
                                html.Hr(),
                            ])
                        ]
                    ),
                ]
            ),
        ]
    ),
    className="mt-3",
)

IA_tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                className='container-fluid',
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Div(className='col-sm-12', children=[
                                dbc.InputGroup(
                                    [
                                        dbc.Button("Random Agent ID for Infection Tracking",
                                                   id="IA1-input-random-agent-button", n_clicks=0),
                                        dbc.Input(id="IA1-input-random-agent-id", placeholder="Random Agent ID"),
                                    ], style=style_random_bottom
                                ),
                                html.H5([dbc.Badge("new_infection.csv:", className="ms-1"),
                                         ' The information when the agent first get exposed.'], style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA1-random-new-infection-figure'),
                                html.H5([dbc.Badge("disease_transition.csv:", className="ms-1"),
                                         ' The infection information of the agent in its life time.'],
                                        style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA1-random-disease-transition-figure'),
                                html.H5([dbc.Badge("activity_history.csv:", className="ms-1"),
                                         ' The activity history information of the agent in its life time.'],
                                        style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA1-random-activity-history-figure'),
                            ]),
                            html.Br(),
                            html.Div(style=style_data_align_0, children=[
                                dbc.Badge("Agent Infection Behavioral Tracking", text_color="dark", color="light",
                                          className="me-1", style=style_badge3),
                                html.H5([
                                    dbc.Badge("Instruction", className="ms-1"),
                                    " Tracking and analyzing the agent's activity and location after it gets infected."
                                ]),
                                html.Div(id='IA1-tracking-by-agent-id-list-group')
                            ]),
                        ]
                    ),
                ]
            ),
        ]
    ),
    className="mt-3",
)

IA_tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                className='container-fluid',
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Div(className='col-sm-12', children=[
                                dbc.InputGroup(
                                    [
                                        dbc.Button("Random Agent ID for Infection Tracking",
                                                   id="IA2-input-random-agent-button", n_clicks=0),
                                        dbc.Input(id="IA2-input-random-agent-id", placeholder="Random Agent ID"),
                                    ], style=style_random_bottom
                                ),
                                html.H5([dbc.Badge("new_infection.csv:", className="ms-1"),
                                         ' The information when the agent first get exposed.'], style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA2-random-new-infection-figure'),
                                html.H5([dbc.Badge("disease_transition.csv:", className="ms-1"),
                                         ' The infection information of the agent in its life time.'],
                                        style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA2-random-disease-transition-figure'),
                                html.H5([dbc.Badge("activity_history.csv:", className="ms-1"),
                                         ' The activity history information of the agent in its life time.'],
                                        style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA2-random-activity-history-figure'),
                            ]),
                            html.Br(),
                            html.Div(style=style_data_align_0, children=[
                                dbc.Badge("Agent Infection Behavioral Tracking", text_color="dark", color="light",
                                          className="me-1", style=style_badge3),
                                html.H5([
                                    dbc.Badge("Instruction", className="ms-1"),
                                    " Tracking and analyzing the agent's activity and location after it gets infected."
                                ]),
                                html.Div(id='IA2-tracking-by-agent-id-list-group')
                            ]),
                        ]
                    ),
                ]
            ),
        ]
    ),
    className="mt-3",
)

IA_tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                className='container-fluid',
                children=[
                    html.Div(
                        className='row',
                        children=[
                            html.Div(className='col-sm-12', children=[
                                dbc.InputGroup(
                                    [
                                        dbc.Button("Random Agent ID for Infection Tracking",
                                                   id="IA3-input-random-agent-button", n_clicks=0),
                                        dbc.Input(id="IA3-input-random-agent-id", placeholder="Random Agent ID"),
                                    ], style=style_random_bottom
                                ),
                                html.H5([dbc.Badge("new_infection.csv:", className="ms-1"),
                                         ' The information when the agent first get exposed.'], style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA3-random-new-infection-figure'),
                                html.H5([dbc.Badge("disease_transition.csv:", className="ms-1"),
                                         ' The infection information of the agent in its life time.'],
                                        style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA3-random-disease-transition-figure'),
                                html.H5([dbc.Badge("activity_history.csv:", className="ms-1"),
                                         ' The activity history information of the agent in its life time.'],
                                        style=style_title),
                                dcc.Graph(style=style_data_align_4, id='IA3-random-activity-history-figure'),
                            ]),
                            html.Br(),
                            html.Div(style=style_data_align_0, children=[
                                dbc.Badge("Agent Infection Behavioral Tracking", text_color="dark", color="light",
                                          className="me-1", style=style_badge3),
                                html.H5([
                                    dbc.Badge("Instruction", className="ms-1"),
                                    " Tracking and analyzing the agent's activity and location after it gets infected."
                                ]),
                                html.Div(id='IA3-tracking-by-agent-id-list-group')
                            ]),
                        ]
                    ),
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
                    dbc.Tabs(
                        [
                            dbc.Tab(IA_tab1_content, label="Model One"),
                            dbc.Tab(IA_tab2_content, label="Model Two"),
                            dbc.Tab(IA_tab3_content, label="Model Three"),
                        ], style={'marginTop': '5px'}
                    )
                ]
            ),
        ]
    ),
    className="mt-3",
)


# Mask Analysis for Model One
MA_tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                className='container-fluid',
                children=[
                    html.Div(
                        className='container-fluid',
                        children=[
                            html.Div(
                                className='row',
                                children=[
                                    html.Div(className='col-sm-4', children=[
                                        html.H5("Model One"),
                                        dcc.Graph(style=style_title, id="MBA1-time-series-chart"),
                                        html.Br(),
                                        html.P(style=style_title, children="Select Cases"),
                                        dcc.Checklist(
                                            style=style_title,
                                            id="MBA1-ticker",
                                            options=["no_mask", "surgical_mask", "n95_mask"],
                                            value=["no_mask", "surgical_mask", "n95_mask"],
                                            inline=True
                                        ),
                                        html.Hr(),
                                    ]),
                                    html.Div(className='col-sm-4', children=[
                                        html.H5("Model Two"),
                                        dcc.Graph(style=style_title, id="MBA2-time-series-chart"),
                                        html.Br(),
                                        html.P(style=style_title, children="Select Cases"),
                                        dcc.Checklist(
                                            style=style_title,
                                            id="MBA2-ticker",
                                            options=["no_mask", "surgical_mask", "n95_mask"],
                                            value=["no_mask", "surgical_mask", "n95_mask"],
                                            inline=True
                                        ),
                                        html.Hr(),
                                    ]),
                                    html.Div(className='col-sm-4', children=[
                                        html.H5("Model Three"),
                                        dcc.Graph(style=style_title, id="MBA3-time-series-chart"),
                                        html.Br(),
                                        html.P(style=style_title, children="Select Cases"),
                                        dcc.Checklist(
                                            style=style_title,
                                            id="MBA3-ticker",
                                            options=["no_mask", "surgical_mask", "n95_mask"],
                                            value=["no_mask", "surgical_mask", "n95_mask"],
                                            inline=True
                                        ),
                                        html.Hr(),
                                    ])
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    ),
    className="mt-3",
)

# Mask Analysis for Effectiveness for Masks
MA_tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                className='container-fluid',
                children=[
                    html.H4([dbc.Badge('Infection by Location under Different Mask-wearing Scenarios', id='LMGBC-ticker')]),
                    dcc.Graph(id="location-mask-grouped-bar-chart"),
                    # html.H4([dbc.Badge('Analysis among Evacuation', id='')]),
                    # #
                    # dcc.Graph(id=''),
                    # #
                    # dcc.Graph(id=''),
                ]
            ),
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                children=[
                    dbc.Tabs(
                        [
                            dbc.Tab(MA_tab1_content, label="Mask-wearing Cases"),
                            dbc.Tab(MA_tab4_content, label="Effectiveness of Mask-wearing"),
                        ], style={'marginTop': '5px'}
                    )
                ]
            ),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Facts"),
        dbc.Tab(tab2_content, label="Infection Rate"),
        dbc.Tab(tab3_content, label="Agent Behavior Tracking"),
        dbc.Tab(tab4_content, label="Mask Analysis"),
        dbc.Tab("tab4_content", label="To be developed", disabled=True),
    ], style={'marginTop': '5px'}
)

layout = html.Div(style=style_data_align_0, children=[
    html.Div(
        children=[
            html.H3("Model Comparison for Infection Part", style=style_select_case),
            tabs
        ]
    ),
])

@callback(
    Output("location-mask-grouped-bar-chart", "figure"),
    Input("LMGBC-ticker", "value")
)
def location_mask_grouped_bar_chart(ticker):
    fig = get_infection_by_location_figure(ModelOne(), ModelTwo(), ModelThree())
    return fig


@callback(
    Output("IP1-time-series-chart", "figure"),
    Input("IP1-ticker", "value"))
def IP1_display_time_series(ticker):
    f = ModelOne()
    return IP_return_time_series(f, ticker)

@callback(
    Output("IP2-time-series-chart", "figure"),
    Input("IP2-ticker", "value"))
def IP2_display_time_series(ticker):
    f = ModelTwo()
    return IP_return_time_series(f, ticker)


@callback(
    Output("IP3-time-series-chart", "figure"),
    Input("IP3-ticker", "value"))
def IP3_display_time_series(ticker):
    f = ModelThree()
    return IP_return_time_series(f, ticker)


@callback(
    Output("MBA1-time-series-chart", "figure"),
    Input("MBA1-ticker", "value"))
def IP1_display_time_series(ticker):
    f = ModelOne()
    return MBA_return_time_series(f, ticker)

@callback(
    Output("MBA2-time-series-chart", "figure"),
    Input("MBA2-ticker", "value"))
def IP2_display_time_series(ticker):
    f = ModelTwo()
    return MBA_return_time_series(f, ticker)


@callback(
    Output("MBA3-time-series-chart", "figure"),
    Input("MBA3-ticker", "value"))
def IP3_display_time_series(ticker):
    f = ModelThree()
    return MBA_return_time_series(f, ticker)


@callback(
    Output("IA1-input-random-agent-id", "value"),
    [Input("IA1-input-random-agent-button", "n_clicks")],
)
def IA1_random_agent_infection(n_clicks):
    f = ModelOne()
    return IA_random_agent_infection(f, n_clicks)


@callback(
    Output("IA1-random-activity-history-figure", "figure"),
    [Input("IA1-input-random-agent-id", "value")]
)
def IA1_return_random_activity_history_table(random_id):
    f = ModelOne()
    return IA_return_random_activity_history_table(f, random_id)


@callback(
    Output("IA1-random-disease-transition-figure", "figure"),
    [Input("IA1-input-random-agent-id", "value")]
)
def IA1_return_random_disease_transition_table(random_id):
    f = ModelOne()
    return IA_return_random_disease_transition_table(f, random_id)


@callback(
    Output("IA1-tracking-by-agent-id-list-group", "children"),
    [Input("IA1-input-random-agent-id", "value")]
)
def IA1_return_random_activity_history_list_group(random_id):
    f = ModelOne()
    return IA_return_random_activity_history_list(f, random_id)


@callback(
    Output("IA1-random-new-infection-figure", "figure"),
    [Input("IA1-input-random-agent-button", "n_clicks")]
)
def IA1_return_random_new_infection_figure(n_clicks):
    f = ModelOne()
    return IA_return_random_new_infection_figure(f, n_clicks)


# ----------------

@callback(
    Output("IA2-input-random-agent-id", "value"),
    [Input("IA2-input-random-agent-button", "n_clicks")],
)
def IA2_random_agent_infection(n_clicks):
    f = ModelTwo()
    return IA_random_agent_infection(f, n_clicks)


@callback(
    Output("IA2-random-activity-history-figure", "figure"),
    [Input("IA2-input-random-agent-id", "value")]
)
def IA2_return_random_activity_history_table(random_id):
    f = ModelTwo()
    return IA_return_random_activity_history_table(f, random_id)


@callback(
    Output("IA2-random-disease-transition-figure", "figure"),
    [Input("IA2-input-random-agent-id", "value")]
)
def IA2_return_random_disease_transition_table(random_id):
    f = ModelTwo()
    return IA_return_random_disease_transition_table(f, random_id)


@callback(
    Output("IA2-tracking-by-agent-id-list-group", "children"),
    [Input("IA2-input-random-agent-id", "value")]
)
def IA2_return_random_activity_history_list_group(random_id):
    f = ModelTwo()
    return IA_return_random_activity_history_list(f, random_id)


@callback(
    Output("IA2-random-new-infection-figure", "figure"),
    [Input("IA2-input-random-agent-button", "n_clicks")]
)
def IA2_return_random_new_infection_figure(n_clicks):
    f = ModelTwo()
    return IA_return_random_new_infection_figure(f, n_clicks)


# -------------------


@callback(
    Output("IA3-input-random-agent-id", "value"),
    [Input("IA3-input-random-agent-button", "n_clicks")],
)
def IA3_random_agent_infection(n_clicks):
    f = ModelThree()
    return IA_random_agent_infection(f, n_clicks)


@callback(
    Output("IA3-random-activity-history-figure", "figure"),
    [Input("IA3-input-random-agent-id", "value")]
)
def IA3_return_random_activity_history_table(random_id):
    f = ModelThree()
    return IA_return_random_activity_history_table(f, random_id)


@callback(
    Output("IA3-random-disease-transition-figure", "figure"),
    [Input("IA3-input-random-agent-id", "value")]
)
def IA3_return_random_disease_transition_table(random_id):
    f = ModelThree()
    return IA_return_random_disease_transition_table(f, random_id)


@callback(
    Output("IA3-tracking-by-agent-id-list-group", "children"),
    [Input("IA3-input-random-agent-id", "value")]
)
def IA3_return_random_activity_history_list_group(random_id):
    f = ModelThree()
    return IA_return_random_activity_history_list(f, random_id)


@callback(
    Output("IA3-random-new-infection-figure", "figure"),
    [Input("IA3-input-random-agent-button", "n_clicks")]
)
def IA3_return_random_new_infection_figure(n_clicks):
    f = ModelThree()
    return IA_return_random_new_infection_figure(f, n_clicks)


@callback(
    Output('facts-model-one', 'children'),
    Input('facts-input-model-one', 'value')
)
def facts_return_model_one(value):
    f = ModelOne()
    return facts_return_html(f)


@callback(
    Output('facts-model-two', 'children'),
    Input('facts-input-model-two', 'value')
)
def facts_return_model_two(value):
    f = ModelTwo()
    return facts_return_html(f)


@callback(
    Output('facts-model-three', 'children'),
    Input('facts-input-model-three', 'value')
)
def facts_return_model_three(value):
    f = ModelThree()
    return facts_return_html(f)
