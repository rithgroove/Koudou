import plotly.graph_objects as go
from ..css import *
import math
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from .global_util import *
import plotly.express as px
from .infection_util import *

def facts_return_html(model):
    df_new_infection = model.new_infection
    df_disease_transition = model.disease_transition
    p1, p2, p3, p4, p5, p6, p7, p8, total_agents, p9, l9, l10, l11, l12 = calculate_facts(df_new_infection, df_disease_transition)
    return html.Div(style=style_data_align_4, children=[
        dbc.Badge("Parameter 1", className="ms-1"),
        html.H5("Avg time when first get exposed:"),
        html.H5(timestamp_converter(math.floor(p1))),
        dbc.Badge("Parameter 2", className="ms-1"),
        html.H5(" Avg time from exposed to asymptomatic: "),
        html.H5(timestamp_converter(math.floor(p2))),
        dbc.Badge("Parameter 3", className="ms-1"),
        html.H5("Avg time from asymptomatic to symptomatic:"),
        html.H5(timestamp_converter(math.floor(p3))),
        dbc.Badge("Parameter 4", className="ms-1"),
        html.H5("Avg time from asymptomatic to recovered:"),
        html.H5(timestamp_converter(math.floor(p4))),
        dbc.Badge("Parameter 5", className="ms-1"),
        html.H5("Avg time from symptomatic to recovered:"),
        html.H5(timestamp_converter(math.floor(p5))),
        dbc.Badge("Parameter 6", className="ms-1"),
        html.H5("Avg time from symptomatic to severe: "),
        html.H5(timestamp_converter(math.floor(p6))),
        dbc.Badge("Parameter 7", className="ms-1"),
        html.H5("Avg time from severe to recovered: "),
        html.H5(timestamp_converter(math.floor(p7))),
        dbc.Badge("Parameter 8", className="ms-1"),
        html.H5("Percentage of agents (" + str(total_agents) +
                " agents in total) never get infected in this life cycle: " + str(p8) + "%"),
        dbc.Badge("Parameter 9", className="ms-1"),
        html.H5("List and number of agent that get infected multiples times:"),
        html.H5(str(p9) + ' agent(s) got infected multiples times, and they are ' + str(l9)),
        dbc.Badge("Parameter 10", className="ms-1"),
        html.H5("Most frequent locations that make agents transfer from exposed to asymptomatic: "),
        html.H5("The locations are lists by their frequency from high to low: "),
        html.H5(str(l10)),
        dbc.Badge("Parameter 11", className="ms-1"),
        html.H5("Most frequent locations that make agents transfer from asymptomatic to symptomatic: "),
        html.H5("The locations are lists by their frequency from high to low: "),
        html.H5(str(l11)),
        dbc.Badge("Parameter 12", className="ms-1"),
        html.H5("Most frequent locations that the agents get exposed: "),
        html.H5("The locations are lists by their frequency from high to low: "),
        html.H5(str(l12)),
    ])

def IA_return_random_new_infection_figure(model, n_clicks):
    df_new_infection = model.new_infection
    infection_agent_id_list = build_infection_agent_list(df_new_infection)
    # initiate and show the first id
    random_id = infection_agent_id_list[0]
    if n_clicks:
        id_list = infection_agent_id_list
        which = n_clicks % len(id_list)
        random_id = id_list[which]
        # random_id = infection_agent_id_list[random.randint(0, len(infection_agent_id_list)-1)]

    agent_pd = agent_id_filter(df_new_infection, random_id)

    agent_pd = df_timestamp_converter(agent_pd)
    column_name_values = ['Agent ID', 'Time Stamp', 'Type', 'Disease', 'Profession',
                          'Location', 'Current Mask', 'Next Mask']
    column_name_list = ['agent_id', 'time_stamp', 'type', 'disease_name', 'agent_profession',
                        'agent_location', 'current_mask', 'next_mask']

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
        height=120,
        # width=80,
        showlegend=False,
        margin=go.layout.Margin(l=0, r=0, b=0, t=5, pad=0),  # pad参数是刻度与标签的距离
    )

    return fig


def IA_return_random_activity_history_list(model, random_id):
    df_disease_transition = model.disease_transition
    df_activity_history = model.activity_history
    df_new_infection = model.new_infection
    infection_agent_id_list = build_infection_agent_list(df_new_infection)
    component_list = [
        dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5("Sample List [Time Stamp]: [Disease Name] Infection State", className="mb-1"),
                        html.Small("Infection Transition: [Current State] -> [Next State]", className="text-success"),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.P("Agent Location at [Location]", className="mb-1"),
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
        agent_activity_html_list = []
        for j in range(len(table)):
            behavioral_sentence = "At " + timestamp_converter(table.iloc[j, 1]) + ", the agent " + \
                                  str(table.iloc[j, 2]) + " " + str(table.iloc[j, 8]) + ', the location is ' \
                                  + table.iloc[j, 4] + '.'
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
                            html.H5(
                                timestamp_converter(time_stamp_list[i]) + ": " + disease_list[i] + " Infection State",
                                className="mb-1"),
                            html.Small("Infection Transition: " + current_state_list[i] + " -> " + next_state_list[i],
                                       className="text-success"),
                        ],
                        className="d-flex w-100 justify-content-between",
                    ),
                    html.P("Agent Location when infection state changes is " + location_list[i], className="mb-1"),
                    html.Div(children=agent_activity_html_list)
                ]
            ),
        )

    # Add tracking information for the last state.
    table = activity_history_pd.loc[(activity_history_pd['time_stamp'] >= time_stamp_list[len(time_stamp_list) - 1])]
    agent_activity_html_list = []
    for j in range(len(table)):
        behavioral_sentence = "At " + timestamp_converter(table.iloc[j, 1]) + ", the agent " + \
                              str(table.iloc[j, 2]) + " " + str(table.iloc[j, 8]) + ', the location is ' \
                              + table.iloc[j, 4] + '.'

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
                        html.H5(timestamp_converter(time_stamp_list[len(time_stamp_list) - 1]) + ": " +
                                disease_list[len(time_stamp_list) - 1] + " Infection State", className="mb-1"),
                        html.Small("Infection Transition: " + current_state_list[len(time_stamp_list) - 1] + " -> "
                                   + next_state_list[len(time_stamp_list) - 1], className="text-success"),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.P("Agent Location when infection state changes is " + location_list[len(time_stamp_list) - 1],
                       className="mb-1"),
                html.Div(children=agent_activity_html_list)
            ]
        ),
    )
    return dbc.ListGroup(component_list)


def IA_return_random_activity_history_table(model, random_id):
    df_new_infection = model.new_infection
    df_activity_history = model.activity_history
    infection_agent_id_list = build_infection_agent_list(df_new_infection)
    if random_id is "":
        agent_pd = agent_id_filter(df_activity_history, infection_agent_id_list[0])
    else:
        agent_pd = agent_id_filter(df_activity_history, random_id)

    agent_pd = df_timestamp_converter(agent_pd)
    column_name_values = ['Time Stamp', 'Profession', 'Location', 'Household ID', 'Activity Name', 'Mask-wearing']
    column_name_list = ['time_stamp', 'profession', 'location', 'household_id', 'activy_name', 'mask_behavior']

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


def IA_return_random_disease_transition_table(model, random_id):
    df_new_infection = model.new_infection
    df_disease_transition = model.disease_transition
    infection_agent_id_list = build_infection_agent_list(df_new_infection)
    if random_id is "":
        agent_pd = agent_id_filter(df_disease_transition, infection_agent_id_list[0])
    else:
        agent_pd = agent_id_filter(df_disease_transition, random_id)

    agent_pd = df_timestamp_converter(agent_pd)
    column_name_values = ['Time Stamp', 'Disease', 'Profession', 'Location',
                          'Current State', 'Next State', 'Mask-wearing']
    column_name_list = ['time_stamp', 'disease_name', 'agent_profession', 'agent_location',
                        'current_state', 'next_state', 'mask_behavior']

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
    return fig

def IA_random_agent_infection(model, n_clicks):
    df_new_infection = model.new_infection
    infection_agent_id_list = build_infection_agent_list(df_new_infection)
    if n_clicks:
        id_list = infection_agent_id_list
        which = n_clicks % len(id_list)
        return id_list[which]
    else:
        return ""


def IP_return_time_series(model, ticker):
    fig = px.line(model.infection_summary, x='time_stamp', y=ticker)
    fig.update_layout(
        plot_bgcolor='#E6E6FA',  # 图的背景颜色
        # paper_bgcolor='#F8F8FF',  # 图像的背景颜色
        height=500,
        showlegend=True,
        margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=0),  # pad参数是刻度与标签的距离
        legend=dict(
            #     orientation="h",  # 控制水平显示
            yanchor="bottom",  # 分别设置xy轴的位置和距离大小
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


def MBA_return_time_series(model, ticker):
    fig = px.line(model.mask_summary, x='time_stamp', y=ticker)
    fig.update_layout(
        plot_bgcolor='#E6E6FA',  # 图的背景颜色
        # paper_bgcolor='#F8F8FF',  # 图像的背景颜色
        height=500,
        showlegend=True,
        margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=0),  # pad参数是刻度与标签的距离
        legend=dict(
            #     orientation="h",  # 控制水平显示
            yanchor="bottom",  # 分别设置xy轴的位置和距离大小
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig
