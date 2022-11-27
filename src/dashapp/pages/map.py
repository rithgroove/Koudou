import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os

style_title = {
    'textAlign': 'center',
}

style_business_map = {
    'margin-left': "10%",
    'margin-right': "10%",
}

style_map_figure = {
    'display': 'center',
    'width': '30%',
    'margin-left': '1.51515%',
    'margin-right': '1.51515%',
    'margin-bottom': '2.5%',
    # 'padding': '5%'
}

dash.register_page(__name__)

business_map = pd.read_csv(os.getcwd()+'../../../config/map/business.csv')
tsukuba_map = pd.read_csv(os.getcwd()+'../../../config/map/tsukuba-tu-building-data.csv')
evacuation_map = pd.read_json(os.getcwd()+'../../../config/map/evacuation_center.json',
                              encoding='utf-8',
                              orient="records")

layout = html.Div(
    children=[
        html.H3("Map Data", style=style_title, id='choice'),
        html.Div(
           children=[
               html.Br(),
               html.Img(src=dash.get_asset_url('full_map.png'), style=style_map_figure),
               html.Img(src=dash.get_asset_url('map_no_zoom.png'), style=style_map_figure),
               html.Img(src=dash.get_asset_url('map_zoom_out.png'), style=style_map_figure),
           ]
        ),
        html.H3("Business Characteristic", style=style_title),
        dcc.Graph(style=style_business_map, id='business-map-show'),
        html.Br(),
        html.H3("Business and Location", style=style_title),
        dcc.Graph(style=style_business_map, id='tsukuba-tu-building-map-show'),
        html.Br(),
        html.H3("Evacuation Center", style=style_title),
        dcc.Graph(style=style_business_map, id='evacuation-center-map-show'),
        html.Br(),
        html.H3("Query Commercial Institution", style=style_title),
        html.Br(),
    ]
)

@callback(Output('evacuation-center-map-show', 'figure'),
          Input('choice', 'value'))
def update_graph(choice):
    value_list = []
    for i in range(len(evacuation_map)):
        single_list = []
        single_list.append(i+1)
        single_list.append(evacuation_map.iloc[i][0]["selection"])
        single_list.append(evacuation_map.iloc[i][0]["rules"]["place_id"])
        single_list.append(evacuation_map.iloc[i][0]["attributes"]["name"])
        single_list.append(evacuation_map.iloc[i][0]["attributes"]["capacity"])
        single_list.append(evacuation_map.iloc[i][0]["attributes"]["contains_food"])
        single_list.append(evacuation_map.iloc[i][0]["attributes"]["contains_medicine"])
        value_list.append(single_list)

    value_list = [[row[col] for row in value_list] for col in range(len(value_list[0]))]
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Center No. \ Values", "Selection", "Place ID", "Name",
                            "Capacity", "Contains Food", "Contains Medicine"],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=value_list,  # 2nd column
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    ])

    fig.update_layout(
        width=1000,
        height=400,
        showlegend=False,
        margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
        )
    return fig

@callback(Output('tsukuba-tu-building-map-show', 'figure'),
          Input('choice', 'value'))
def update_graph(choice):
    column_name_values = ['y-axis', 'x-axis', 'Number', 'Business Type']
    column_name_list = ['y', 'x', 'number', 'type']
    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.5,
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
                values=[tsukuba_map[k].tolist() for k in column_name_list],
                align="left"),
        ),
        row='all', col='all'
    ),
    fig.update_layout(
        plot_bgcolor='#E6E6FA',  # 图的背景颜色
        paper_bgcolor='#F8F8FF',  # 图像的背景颜色
        height=500,
        width=1000,
        showlegend=False,
        margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig

@callback(Output('business-map-show', 'figure'),
          Input('choice', 'value'))
def update_graph(choice):
    column_name_values = ['Building', 'Min Workhour', 'Max Workhour', 'Min Starthour', 'Max Starhour', 'Day',
                          'Min Activity Perweek', 'Max Activity Perweek', 'Open 24Hour Chance']
    column_name_list = ['building_type', 'min_workhour', 'max_workhour', 'min_start_hour',
                        'max_start_hour', 'day', 'min_activity_per_week', 'max_activity_per_week', 'open_24_hours_chance']
    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.5,
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
                values=[business_map[k].tolist() for k in column_name_list],
                align="left"),
        ),
        row='all', col='all'
    ),
    fig.update_layout(
        plot_bgcolor='#E6E6FA',  # 图的背景颜色
        paper_bgcolor='#F8F8FF',  # 图像的背景颜色
        height=200,
        width=1000,
        showlegend=False,
        margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig
