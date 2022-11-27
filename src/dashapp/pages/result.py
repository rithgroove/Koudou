import dash
from dash import html
import os

style_title = {
    'textAlign': 'center',
    'marginLeft': '100px',
    'marginRight': '100px',
}

style_log = {
    # 'textAlign': 'center',
    'marginLeft': '100px',
    'marginRight': '100px',
}

style_dropdown = {
    'width': '250px'
}

log_data = open(os.getcwd()+'/data/log_result/log.txt')
log_data_lines = log_data.readlines()


dash.register_page(__name__)

html_list = []
for i in range(len(log_data_lines)):
    html_list.append(html.H5(log_data_lines[i]))

layout = html.Div(
    children=[
        html.Br(),
        html.H3('Log Information for Simulator', style=style_title),
        html.Br(),
        html.Div(style=style_log,
            children=html_list
        )
    ]
)

