from dash import html
import plotly.graph_objects as go
import pandas as pd

# ---------------- config ------------------
def config_tables_show():

    pass

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


# ---------------- infection ------------------
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
