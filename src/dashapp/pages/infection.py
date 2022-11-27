import datetime
import dash
from dash import dcc, Input, Output, callback
import plotly.express as px
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .public.css import *
from .public.data import *
from .public.utils import *

style_checkList = {
    'textAlign': 'center'
}

style_div_left = {
    'float': 'left',
    'width': '48%',
    'marginLeft': '1%',
}

style_div_right= {
    'float': 'right',
    'width': '48%',
    'marginRight': '1%',
}

style_interactive_button = {
    'width': '48%',
    'marginLeft': '1%',
}

style_interactive_table={
    'margin-left': '-50px'
}

style_form={
    'float': 'right'
}

style_radio = {
    'margin-left': '10px'
}

style_download_button = {
    'margin': '30px'
}

dash.register_page(__name__)

df_demo1 = pd.read_csv(os.getcwd() + './data/infection_summary_demo1.csv')
df_demo2 = pd.read_csv(os.getcwd() + './data/infection_summary_demo2.csv')
df_disease_transition = pd.read_csv(os.getcwd() + './data/disease_transition.csv')
df_activity_history = pd.read_csv(os.getcwd() + './data/activity_history.csv')
df_new_infection = pd.read_csv(os.getcwd() + './data/new_infection.csv')

layout = html.Div(children=[
    html.Div([

        html.Div(
            children=[
                html.H2(style=style_title, children="Infection Analytics"),
                html.H3(style=style_title, id='datetime-text'),
                dcc.Interval(
                    id='datetime',
                    interval=20*1000,
                    n_intervals=0
                )
            ]
        ),

        html.Div(style=style_div_left, children=[
            # html.Img(src='https://askabiologist.asu.edu/sites/default/files/headers/covidsim-header_0.png', alt="Model Introduction Picture"),
            # dcc.Markdown(children=markdown_text),

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
            dcc.Graph(style=style_interactive_table, id='indicator-graphic'),
        ]),


        html.Div(style=style_div_right, children=[
            html.H4(style=style_title, children="Infection Situation by Time"),
            dcc.Graph(style=style_title, id="time-series-chart"),
            html.P(style=style_title, children="Select a Case"),
            dcc.Checklist(
                style=style_checkList,
                id="ticker",
                options=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe", "recovered"],
                value=["susceptible", "exposed", "asymptomatic", "symptomatic", "severe", "recovered"],
                inline=True
            ),
            html.Button("Download Source File", id="btn_image", style=style_download_button),
            dcc.Download(id="download-image"),
            html.H4(style=style_title, children='Show Result in Form'),
            generate_table(df_demo2),
            html.Br(),

            dcc.Graph(style=style_interactive_table, id='pie-chart'),
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

])


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
    fig = px.line(df_demo1, x='time_stamp', y=ticker)
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
        height=1300,
        width=700,
        showlegend=False,
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
    return fig

@callback(
    Output("download-image", "data"),
    Input("btn_image", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_demo1.to_csv, "infection_demo_download.csv")

