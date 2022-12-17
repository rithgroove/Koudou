import plotly.graph_objects as go
import io
import base64
import datetime
import pandas as pd
from dash import html, dash_table
import numpy as np
import parameters.default as defaultParam
from src.util.time_stamp import TimeStamp
from .File_Factory import ModelOne, ModelTwo, ModelThree
from collections import Counter
from .css import *
import time


# ---------------- global ------------------
def timestamp_converter(timestamp):
    ts = TimeStamp(timestamp)
    time = '[' + str(ts.get_week()) + ' week ' + str(ts.get_day_of_week()) + ' days ' + str(ts.get_hour_min_str()) \
           + ':' + str(ts.get_second()) + ']'
    return time


def df_timestamp_converter(df):
    df.index = range(len(df))
    for i in range(len(df)):
        df.loc[i, 'time_stamp'] = timestamp_converter(df.loc[i, 'time_stamp'])
    return df


# ---------------- config ------------------
def table_generator(target_dataframe):
    column_list = []
    for item in target_dataframe.columns:
        column_list.append(target_dataframe[item])
    fig = go.Figure(
        data=[go.Table(
            header=dict(values=list(target_dataframe.columns),  # 表头取值是data列属性
                        fill_color='paleturquoise',  # 填充色和文本位置
                        align='left'),
            cells=dict(values=column_list,  # 单元格的取值就是每个列属性的Series取值
                       fill_color='lavender',
                       align='left'
                       )
        )]
    )
    return fig


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


# ---------------- map ------------------
def build_option_list(tsukuba_map):
    return tsukuba_map['type'].unique().tolist()


def count_business_number(filter_list, filer_df):
    dict_result = {}
    for item in filter_list:
        target_len = len(filer_df.loc[filer_df['type'] == item])
        dict_result[item] = target_len
    return dict_result


def build_map_data_table():
    pass


# ---------------- infection ------------------
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
            ts_start = df_new_infection.loc[df_new_infection['agent_id'] == agent_id].iloc[0, 0]
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

    return p1, p2, p3, p4, p5, p6, p7, p8, total_agents, p9, l9, result_counter1, result_counter2


def build_infection_agent_list(new_infection):
    return new_infection['agent_id'].unique().tolist()


def agent_id_filter(data_df, agent_id):
    return data_df.loc[data_df['agent_id'] == agent_id]


def preprocess_linear_data():
    pass


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


# ---------------- evacuation ------------------
def find_single_agent_path():
    pass


# ---------------- location ------------------
def location_divider(df_agent_position_summary):
    list_locations = []
    unique_location_list = df_agent_position_summary['location'].unique()

    for location in unique_location_list:
        this_location_list = df_agent_position_summary.loc[df_agent_position_summary['location'] == location]
        list_locations.append(this_location_list)

    df_comp = location_df_processor(list_locations)
    return df_comp


def location_df_processor(position_list):
    init_df = position_list[0]
    init_df.drop(['location'], axis=1)
    init_df.rename(columns={'count': 'home'})
    for df in position_list:
        pass
    return position_list


def proportion_calculation(df):
    result_dict = {}
    timestamp_length = int(df.loc[len(df) - 1, 'time_stamp']) / 5
    unique_location_list = df['location'].unique()
    for location in unique_location_list:
        single_location_df = df.loc[df['location'] == location]
        mean_count = np.sum(single_location_df['count']) / timestamp_length
        result_dict[location] = round(mean_count, 2)

    return result_dict


# ---------------- upload ------------------
def parse_contents(contents, filename, date, f):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            if 'activity_history.' in filename:
                f.activity_history = df
            elif 'agent_position_summary.' in filename:
                f.agent_position_summary = df
            elif 'disease_transition.' in filename:
                f.disease_transition = df
            elif 'evacuation.' in filename:
                f.evacuation = df
            elif 'infection_summary' in filename:
                f.infection_summary = df
            elif 'infection_transition.' in filename:
                f.infection_transition = df
            elif 'new_infection.' in filename:
                f.new_infection = df
            else:
                return html.Div(['CSV file is not found .'])
        elif 'txt' in filename:
            # Assume that the user uploaded an excel file
            log_data_lines = str(decoded).split('\\n')
            html_list = []
            for i in range(len(log_data_lines)):
                html_list.append(html.H5(log_data_lines[i]))
            f.log = html_list
            # return html.Div(style=style_log, children=html_list)
    except Exception as e:
        print('[Error Log]: ', e)
        return html.Div([
            'There was an error processing this file, please refer to terminal.'
        ])
    return html.Div([
        html.H5('[File Processing ' + time.ctime() + ']: ' + filename + ' is uploaded successfully!',
                style=style_title)
    ])
