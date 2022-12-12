import dash
from dash import dcc, Input, Output, callback
import plotly.express as px
import os
from plotly.subplots import make_subplots
from .public.css import *
from .public.utils import *
import dash_bootstrap_components as dbc
from .public.File_Factory import Files

style_radio = {
    'margin-left': '10px'
}

style_download_button = {
    'margin': '30px'
}

dash.register_page(__name__)

file_object = Files()

# df_demo1 = pd.read_csv(os.getcwd() + './data/infection_summary_demo1.csv')
# df_demo1 = pd.NA
df_demo2 = pd.read_csv(os.getcwd() + './data/infection_summary_demo2.csv')
df_infection_summary = pd.read_csv(os.getcwd() + './data/simulation_result/infection_summary.csv')

df_disease_transition = pd.read_csv(os.getcwd() + './data/simulation_result/disease_transition.csv')
df_activity_history = pd.read_csv(os.getcwd() + './data/simulation_result/activity_history.csv')
df_new_infection = pd.read_csv(os.getcwd() + './data/simulation_result/new_infection.csv')
infection_agent_id_list = build_infection_agent_list(df_new_infection)

layout = html.Div(children=[
    html.Div([
        html.Div(
            children=[
                html.Span('Infection Analysis', className="badge bg-dark", style=style_badge),
                html.H3(style=style_title, id='datetime-text'),
                dcc.Interval(
                    id='datetime',
                    interval=20 * 1000,
                    n_intervals=0
                )
            ]
        ),

        html.Div(style=style_div_left, children=[
            html.H4(style=style_title, children="Joint Search with Result Set"),
            html.Div(style=style_interactive_button, children=[
                html.Label('Profession'),
                dcc.Dropdown(
                    ['University Student', 'Student', 'All'],
                    'All',
                    id='profession'),
            ]),
            html.Br(),
            html.Div(style=style_radio, children=[
                html.Label('File Name'),
                dcc.RadioItems(['New Infection', 'Activity History', 'Disease Transition'],
                               'New Infection',
                               id='file_name'),
            ]
                     ),
            dcc.Graph(style=style_infection_table, id='indicator-graphic'),
        ]),

        html.Div(style=style_div_right, children=[
            html.H4(style=style_title, children="Infection Situation by Time"),
            dcc.Graph(style=style_title, id="time-series-chart"),
            html.P(style=style_title, children="Select a Case"),
            dcc.Checklist(
                style=style_title,
                id="ticker",
                options=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe", "recovered"],
                value=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe", "recovered"],
                inline=True
            ),
            html.Br(),
            html.H4(style=style_title, children='Show Result in Form'),
            generate_table(df_demo2),
            html.Br(),

            dcc.Graph(style=style_infection_table, id='pie-chart'),
            html.Label('Slide for time change'),
            dcc.Slider(
                min=df_demo2['list'].min(),
                max=df_demo2['list'].max(),
                step=None,
                marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 7)},
                value=1,
                id='time-tracker'
            ),
        ])
    ]),
    html.Div(children=[
        html.Span('Infection for Agent', className="badge bg-dark", style=style_badge),
    ]),
    html.Div(style=style_data_table, children=[
        dbc.InputGroup(
            [
                dbc.Button("Random Agent ID for Infection Tracking", id="input-random-agent-button", n_clicks=0),
                dbc.Input(id="input-random-agent-id", placeholder="Random Agent ID"),
            ], style=style_random_bottom
        ),

        html.H5([dbc.Badge("new_infection.csv:", className="ms-1"),
                 ' The information when the agent first get infected.'], style=style_title),
        dcc.Graph(style=style_data_align_4, id='random-new-infection-figure'),
        html.H5([dbc.Badge("disease_transition.csv:", className="ms-1"),
                 ' The infection information of the agent in its life time.'],
                style=style_title),
        dcc.Graph(style=style_data_align_4, id='random-disease-transition-figure'),
        html.H5([dbc.Badge("activity_history.csv:", className="ms-1"),
                 ' The activity history information of the agent in its life time.'],
                style=style_title),
        dcc.Graph(style=style_data_align_4, id='random-activity-history-figure'),
    ]),
    html.Br(),
    html.Div(style=style_data_table, children=[
        dbc.Badge("Agent Infection Behavioral Tracking", text_color="dark", color="light",
                  className="me-1", style=style_badge1),
        html.H5([
            dbc.Badge("Instruction", className="ms-1"),
            " Tracking and analyzing the agent's activity and location after it gets infected."
        ]),
        html.Div(id='tracking-by-agent-id-list-group')
    ])
])


@callback(
    Output("tracking-by-agent-id-list-group", "children"),
    [Input("input-random-agent-id", "value")]
)
def return_random_activity_history_table(random_id):
    component_list = [
        dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5("[Time Stamp]: [Disease Name] Infection State", className="mb-1"),
                        html.Small("Infection Transition: [Current State] -> [Next State]", className="text-success"),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.P("Agent Location at [Time Stamp]: [Location]", className="mb-1"),
                html.Div(
                    [
                        html.Small("At [Time Stamp], the agent [Agent ID] [Activity] at [Location].",
                                   className="text-muted"),
                        html.Br(),
                        html.Small("Finish activities at this infection state period.", className="text-muted"),
                    ]
                )
            ]
        ),
    ]

    if random_id is "":
        disease_transition_pd = agent_id_filter(df_disease_transition, infection_agent_id_list[0])
        activity_history_pd = agent_id_filter(df_activity_history, infection_agent_id_list[0])
    else:
        disease_transition_pd = agent_id_filter(df_disease_transition, random_id)
        activity_history_pd = agent_id_filter(df_activity_history, random_id)

    time_stamp_list = disease_transition_pd['time_stamp'].tolist()
    current_state_list = disease_transition_pd['current_state'].tolist()
    next_state_list = disease_transition_pd['next_state'].tolist()
    disease_list = disease_transition_pd['disease_name'].tolist()
    location_list = disease_transition_pd['agent_location'].tolist()

    for i in range(len(time_stamp_list) - 1):
        table = get_data_by_interval(time_stamp_list[i], time_stamp_list[i + 1], activity_history_pd)

        print(table)

        agent_activity_html_list = []
        for j in range(len(table)):
            behavioral_sentence = "At "+str(table.iloc[j, 0])+", the agent "+\
                                  str(table.iloc[j, 1])+" "+str(table.iloc[j, 7])+'.'

            agent_activity_html_list.append(
                html.Small(behavioral_sentence, className="text-muted"),
            )
            agent_activity_html_list.append(
                html.Br(),
            )

        agent_activity_html_list.append(
                html.Small("Finish activities at this infection state period.", className="text-muted")
        )

        component_list.append(
            dbc.ListGroupItem(
                [
                    html.Div(
                        [
                            html.H5(str(time_stamp_list[i])+": "+disease_list[i]+" Infection State", className="mb-1"),
                            html.Small("Infection Transition: "+current_state_list[i]+" -> "+next_state_list[i],
                                       className="text-success"),
                        ],
                        className="d-flex w-100 justify-content-between",
                    ),
                    html.P("Agent Location when infection state changes is "+location_list[i], className="mb-1"),
                    html.Div(children=agent_activity_html_list)
                ]
            ),
        )
        pass

    return dbc.ListGroup(component_list)


@callback(
    Output("random-activity-history-figure", "figure"),
    [Input("input-random-agent-id", "value")]
)
def return_random_activity_history_table(random_id):
    if random_id is "":
        agent_pd = agent_id_filter(df_activity_history, infection_agent_id_list[0])
    else:
        agent_pd = agent_id_filter(df_activity_history, random_id)

    column_name_values = [
        'Agent ID', 'Time Stamp', 'Profession', 'Location', 'Household ID', 'Activity Name'
    ]
    column_name_list = [
        'agent_id', 'time_stamp', 'profession', 'location', 'household_id', 'activy_name'
    ]

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]]
    )
    fig.add_trace(
        go.Table(
            header=dict(
                values=column_name_values,
                font=dict(size=12),
                align="left"
            ),
            cells=dict(
                values=[agent_pd[k].tolist() for k in column_name_list],
                align="left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=300,
        # width=80,
        showlegend=False,
        margin=go.layout.Margin(l=0, r=0, b=0, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig


@callback(
    Output("random-disease-transition-figure", "figure"),
    [Input("input-random-agent-id", "value")]
)
def return_random_disease_transition_table(random_id):
    if random_id is "":
        agent_pd = agent_id_filter(df_disease_transition, infection_agent_id_list[0])
    else:
        agent_pd = agent_id_filter(df_disease_transition, random_id)

    column_name_values = ['Agent ID', 'Time Stamp', 'Disease', 'Profession', 'Location',
                          'Current State', 'Next State']
    column_name_list = ['agent_id', 'time_stamp', 'disease_name', 'agent_profession', 'agent_location',
                        'current_state', 'next_state']

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]]
    )
    fig.add_trace(
        go.Table(
            header=dict(
                values=column_name_values,
                font=dict(size=12),
                align="left"
            ),
            cells=dict(
                values=[agent_pd[k].tolist() for k in column_name_list],
                align="left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=140,
        # width=80,
        showlegend=False,
        margin=go.layout.Margin(l=0, r=0, b=0, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    # print(random_id)
    return fig


@callback(
    Output("random-new-infection-figure", "figure"),
    [Input("input-random-agent-button", "n_clicks")]
)
def return_random_new_infection_figure(n_clicks):
    # initiate and show the first id
    random_id = infection_agent_id_list[0]
    if n_clicks:
        id_list = infection_agent_id_list
        which = n_clicks % len(id_list)
        random_id = id_list[which]

    agent_pd = agent_id_filter(df_new_infection, random_id)

    column_name_values = ['Agent ID', 'Time Stamp', 'Type', 'Disease', 'Profession',
                          'Location', 'Source Profession', 'Source Location']
    column_name_list = ['agent_id', 'time_stamp', 'type', 'disease_name', 'agent_profession',
                        'agent_location', 'source_profession', 'source_location']

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]]
    )
    fig.add_trace(
        go.Table(
            header=dict(
                values=column_name_values,
                font=dict(size=12),
                align="left"
            ),
            cells=dict(
                values=[agent_pd[k].tolist() for k in column_name_list],
                align="left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=80,
        # width=80,
        showlegend=False,
        margin=go.layout.Margin(l=0, r=0, b=0, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig


@callback(
    Output("input-random-agent-id", "value"),
    [Input("input-random-agent-button", "n_clicks")],
)
def random_agent_infection(n_clicks):
    if n_clicks:
        id_list = infection_agent_id_list
        which = n_clicks % len(id_list)
        return id_list[which]
    else:
        return ""


@callback(
    Output("datetime-text", "children"),
    Input('datetime', "n_intervals")
)
def live_datetime(n):
    return [
        html.H5(str(datetime.datetime.now().ctime()))
    ]


@callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"))
def display_time_series(ticker):
    f = Files()
    # print('f.count from infection.py', f.infection_summary)
    fig = px.line(f.infection_summary, x='time_stamp', y=ticker)
    fig.update_layout(
        plot_bgcolor='#E6E6FA',  # 图的背景颜色
        # paper_bgcolor='#F8F8FF',  # 图像的背景颜色
        height=400,
        width=600,
        showlegend=False,
        margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig


@callback(
    Output('indicator-graphic', 'figure'),
    Input('profession', 'value'),
    Input('file_name', 'value'))
def update_graph(profession, file_name):
    join_df = join_search_profession(profession, file_name, df_new_infection, df_activity_history,
                                     df_disease_transition)
    if file_name == 'New Infection':
        column_name_values = ['time', 'type', 'disease', 'id', 'profession', 'source']
        column_name_list = ['time_stamp', 'type', 'disease_name', 'agent_id', 'agent_profession', 'source_id']
    elif file_name == 'Activity History':
        column_name_values = ['time', 'id', 'profession', 'location', 'household_id',
                              'activity']  # 'id', 'profession', 'location', 'household', 'activity'
        column_name_list = ['time_stamp', 'agent_id', 'profession', 'location', 'household_id',
                            'activity_name']  # 'agent_id', 'profession', 'location', 'household_id', 'activity_name'
    else:
        column_name_values = ['time', 'agent_id', 'disease', 'profession', 'location', 'c-state', 'n-state']
        column_name_list = ['time_stamp', 'agent_id', 'disease_name', 'agent_profession', 'agent_location',
                            'current_state', 'next_state']

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]]
    )
    fig.add_trace(
        go.Table(
            header=dict(
                values=column_name_values,
                font=dict(size=12),
                align="left"
            ),
            cells=dict(
                values=[join_df[k].tolist() for k in column_name_list],
                align="left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=1200,
        width=600,
        showlegend=False,
        margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig


@callback(
    Output("pie-chart", "figure"),
    Input("time-tracker", "value"))
def generate_chart(time_tracker):
    labels = ['susceptible', 'exposed', 'asymptomatic', 'symptomatic', 'severe', 'recovered']
    index = time_tracker - 1
    values = [df_demo2.loc[index, 'susceptible'], df_demo2.loc[index, 'exposed'], df_demo2.loc[index, 'asymptomatic'],
              df_demo2.loc[index, 'symptomatic'], df_demo2.loc[index, 'severe'], df_demo2.loc[index, 'recovered']]
    trace = [go.Pie(labels=labels, values=values)]
    layout = go.Layout(title='Proportion of Infection')
    fig = go.Figure(data=trace, layout=layout)
    fig.update_layout(
        margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig

# @callback(
#     Output("download-agent-analysis", "data"),
#     Input("btn_image", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     return dcc.send_data_frame(df_demo1.to_csv, "infection_demo_download.csv")
