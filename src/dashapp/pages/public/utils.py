import plotly.graph_objects as go
import io
import base64
import datetime
import pandas as pd
from dash import html, dash_table
from .File_Factory import Files

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
def build_infection_agent_list(new_infection):
    return new_infection['agent_id'].unique().tolist()

def track_infection_state_new_infection(new_infection, agent_id):
    return new_infection.loc[new_infection['agent_id'] == agent_id]

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
            result_df = df_new_infection[df_new_infection['agent_profession']=='university_student']
        elif profession == 'All':
            result_df = df_new_infection
        else:
            result_df = df_new_infection[df_new_infection['agent_profession']=='student']
    elif file_name == 'Activity History':
        if profession == 'University Student':
            result_df = df_activity_history[df_activity_history['profession']=='university_student']
        elif profession == 'All':
            result_df = df_activity_history
        else:
            result_df = df_activity_history[df_activity_history['profession']=='student']
    else:
        if profession == 'University Student':
            result_df = df_disease_transition[df_disease_transition['agent_profession']=='university_student']
        elif profession == 'All':
            result_df = df_disease_transition
        else:
            result_df = df_disease_transition[df_disease_transition['agent_profession']=='student']
    return result_df


# ---------------- evacuation ------------------
def find_single_agent_path():
    pass


# ---------------- location ------------------
def location_divider():
    pass


# ---------------- upload ------------------
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            # print(df)
            f = Files()
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
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' in filename:
            df = open(io.BytesIO(decoded))
            df = df.readlines()

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5("Upload Successfully!"),
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

