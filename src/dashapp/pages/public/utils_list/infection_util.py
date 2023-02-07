import parameters.default as defaultParam
import numpy as np
from collections import Counter
from dash import html
import plotly.graph_objects as go

def single_fact_calculator(df_disease_transition, current_state, next_state):
    list = []
    for i in range(len(df_disease_transition)):
        if df_disease_transition.loc[i, 'current_state'] == current_state and df_disease_transition.loc[
            i, 'next_state'] == next_state:
            ts_end = df_disease_transition.loc[i, 'time_stamp']
            agent_id = df_disease_transition.loc[i, 'agent_id']
            ts_temp = 0
            for j in range(i + 1):
                if df_disease_transition.loc[i - j, 'agent_id'] == agent_id and df_disease_transition.loc[
                    i - j, 'next_state'] == current_state:
                    ts_temp = df_disease_transition.loc[i - j, 'time_stamp']
                    break
            if ts_temp == 0:
                pass
            else:
                ts_start = ts_temp
                ts_diff = ts_end - ts_start
                list.append(ts_diff)
    p = np.mean(list)
    return p


def calculate_facts(df_new_infection, df_disease_transition):
    p1 = np.mean(df_new_infection['time_stamp'])
    list_p2 = []
    for i in range(len(df_disease_transition)):
        if df_disease_transition.loc[i, 'current_state'] == 'exposed' and df_disease_transition.loc[
            i, 'next_state'] == 'asymptomatic':
            ts_end = df_disease_transition.loc[i, 'time_stamp']
            agent_id = df_disease_transition.loc[i, 'agent_id']
            ts_start = df_new_infection.loc[df_new_infection['agent_id'] == agent_id].iloc[0, 1]
            ts_diff = ts_end - ts_start
            list_p2.append(ts_diff)
    p2 = np.mean(list_p2)

    p3 = single_fact_calculator(df_disease_transition, 'asymptomatic', 'symptomatic')
    p4 = single_fact_calculator(df_disease_transition, 'asymptomatic', 'recovered')
    p5 = single_fact_calculator(df_disease_transition, 'symptomatic', 'recovered')
    p6 = single_fact_calculator(df_disease_transition, 'symptomatic', 'severe')
    p7 = single_fact_calculator(df_disease_transition, 'severe', 'recovered')

    p8_1 = list(set(df_disease_transition['agent_id']))
    p8_2 = list(set(df_new_infection['agent_id']))
    p8_3 = p8_1 + p8_2
    p8_len = len(list(set(p8_3)))
    total_agents = defaultParam.parameters.get("N_AGENTS")
    p8 = (total_agents - p8_len) / total_agents * 100

    p9 = 0
    l9 = []
    for i in range(len(df_disease_transition)):
        if df_disease_transition.loc[i, 'current_state'] == 'recovered':
            p9 = p9 + 1
            agent_id = df_disease_transition.loc[i, 'agent_id']
            l9.append(agent_id)

    list_location = []
    for i in range(len(df_disease_transition)):
        if df_disease_transition.loc[i, 'current_state'] == 'exposed' and df_disease_transition.loc[
            i, 'next_state'] == 'asymptomatic':
            list_location.append(df_disease_transition.loc[i, 'agent_location'])
    result_counter1 = Counter(list_location)

    list_location = []
    for i in range(len(df_disease_transition)):
        if df_disease_transition.loc[i, 'current_state'] == 'asymptomatic' and df_disease_transition.loc[
            i, 'next_state'] == 'symptomatic':
            list_location.append(df_disease_transition.loc[i, 'agent_location'])
    result_counter2 = Counter(list_location)

    list_location = []
    for i in range(len(df_new_infection)):
        list_location.append(df_new_infection.loc[i, 'agent_location'])
    result_counter3 = Counter(list_location)

    return p1, p2, p3, p4, p5, p6, p7, p8, total_agents, p9, l9, result_counter1, result_counter2, result_counter3


def build_infection_agent_list(new_infection):
    return new_infection['agent_id'].unique().tolist()


def agent_id_filter(data_df, agent_id):
    return data_df.loc[data_df['agent_id'] == agent_id]


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def join_search_profession(profession, file_name, df_new_infection, df_activity_history, df_disease_transition):
    if file_name == 'New Infection':
        if profession == 'University Student':
            result_df = df_new_infection[df_new_infection['agent_profession'] == 'university_student']
        elif profession == 'All':
            result_df = df_new_infection
        else:
            result_df = df_new_infection[df_new_infection['agent_profession'] == 'student']
    elif file_name == 'Activity History':
        if profession == 'University Student':
            result_df = df_activity_history[df_activity_history['profession'] == 'university_student']
        elif profession == 'All':
            result_df = df_activity_history
        else:
            result_df = df_activity_history[df_activity_history['profession'] == 'student']
    else:
        if profession == 'University Student':
            result_df = df_disease_transition[df_disease_transition['agent_profession'] == 'university_student']
        elif profession == 'All':
            result_df = df_disease_transition
        else:
            result_df = df_disease_transition[df_disease_transition['agent_profession'] == 'student']
    return result_df


def text_color():
    pass


def get_data_by_interval(start, end, df):
    df = df.loc[(df['time_stamp'] >= start) & (df['time_stamp'] <= end)]
    return df


def get_location_value(unique_locations, result_counter):
    return_list = []
    for key in unique_locations:
        if key in result_counter.keys():
            return_list.append(result_counter[key])
        else:
            return_list.append(0)
    return return_list

def get_infection_by_location_figure(f1, f2, f3):
    f1_new_infection = f1.new_infection
    f2_new_infection = f2.new_infection
    f3_new_infection = f3.new_infection
    list_location1 = []
    for i in range(len(f1_new_infection)):
        list_location1.append(f1_new_infection.loc[i, 'agent_location'])
    result_counter1 = dict(Counter(list_location1))
    list_location2 = []
    for i in range(len(f2_new_infection)):
        list_location2.append(f2_new_infection.loc[i, 'agent_location'])
    result_counter2 = dict(Counter(list_location2))
    list_location3 = []
    for i in range(len(f3_new_infection)):
        list_location3.append(f3_new_infection.loc[i, 'agent_location'])
    result_counter3 = dict(Counter(list_location3))
    unique_locations = list(set(list_location1+list_location2+list_location3))
    model_one_value = get_location_value(unique_locations, result_counter1)
    model_two_value = get_location_value(unique_locations, result_counter2)
    model_three_value = get_location_value(unique_locations, result_counter3)
    fig = go.Figure(data=[
        go.Bar(name='Model One', x=unique_locations, y=model_one_value),
        go.Bar(name='Model Two', x=unique_locations, y=model_two_value),
        go.Bar(name='Model Three', x=unique_locations, y=model_three_value),
    ])
    fig.update_layout(
        barmode='group',
        plot_bgcolor='#E6E6FA',
        height=600,
        showlegend=True,
        margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=0),
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig
