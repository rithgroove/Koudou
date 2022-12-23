import io
import base64
import pandas as pd
from dash import html
from ..css import *
import time


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
    except Exception as e:
        print('[Error Log]: ', e)
        return html.Div([
            'There was an error processing this file, please refer to terminal.'
        ])
    return html.Div([
        html.H5('[File Processing ' + time.ctime() + ']: ' + filename + ' is uploaded successfully!',
                style=style_title)
    ])
