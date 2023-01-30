# import dash
# from dash import html
# import os
# from .public.css import *
#
# log_data = open(os.getcwd()+'/data/log_result/log.txt')
# log_data_lines = log_data.readlines()
#
# dash.register_page(__name__)
#
# html_list = []
# for i in range(len(log_data_lines)):
#     html_list.append(html.H5(log_data_lines[i]))
#
# layout = html.Div(
#     children=[
#         html.Span('Simulation Log', className="badge bg-dark", style=style_badge),
#         html.Div(style=style_log, children=html_list)
#     ], style=style_background
# )
#
