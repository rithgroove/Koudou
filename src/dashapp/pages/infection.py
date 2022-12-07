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
                    interval=20*1000,
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
            # html.Button("Download Source File", id="btn_image", style=style_download_button),
            # dcc.Download(id="download-image"),
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
    html.Span('Infection for Agent', className="badge bg-dark", style=style_badge),
    html.Div(style=style_data_table, children=[
        dbc.InputGroup(
            [
                dbc.Button("Random Agent ID for Infection Tracking", id="input-random-agent-button", n_clicks=0),
                dbc.Input(id="input-random-agent-id", placeholder="Agent ID"),
            ], style=style_random_bottom
        ),

        dcc.Graph(style=style_data_table, id='random-agent-figure'),
    ]),

])

@callback(
    Output("random-agent-figure", "figure"),
    [Input("input-random-agent-button", "n_clicks")]
)
def agent_report_figure(n_clicks):
    if n_clicks:
        id_list = infection_agent_id_list
        which = n_clicks % len(id_list)
        random_id = id_list[which]
    print(random_id)
    agent_pd = track_infection_state_new_infection(df_new_infection, random_id)
    print(agent_pd)

    column_name_values = ['time', 'Type', 'Disease', 'Profession',
                          'Location', 'Node ID', 'Source ID', 'Source Profession',
                          'Source Location', 'Source Node ID']
    column_name_list = ['time_stamp', 'type', 'disease_name', 'agent_profession',
                        'agent_location', 'agent_node_id', 'source_id', 'source_profession',
                        'source_location', 'source_node_id']

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
        height=1200,
        width=1000,
        showlegend=False,
        margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
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
    print('f.count from infection.py', f.infection_summary)
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
    join_df = join_search_profession(profession, file_name, df_new_infection, df_activity_history, df_disease_transition)
    if file_name == 'New Infection':
        column_name_values = ['time', 'type', 'disease', 'id', 'profession', 'source']
        column_name_list = ['time_stamp', 'type', 'disease_name', 'agent_id', 'agent_profession', 'source_id']
    elif file_name == 'Activity History':
        column_name_values = ['time', 'id', 'profession', 'location', 'household_id', 'activity'] # 'id', 'profession', 'location', 'household', 'activity'
        column_name_list = ['time_stamp', 'agent_id', 'profession', 'location', 'household_id', 'activity_name'] # 'agent_id', 'profession', 'location', 'household_id', 'activity_name'
    else:
        column_name_values = ['time', 'agent_id', 'disease', 'profession', 'location', 'c-state', 'n-state']
        column_name_list = ['time_stamp', 'agent_id', 'disease_name', 'agent_profession', 'agent_location', 'current_state', 'next_state']

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
    layout=go.Layout(title='Proportion of Infection')
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

