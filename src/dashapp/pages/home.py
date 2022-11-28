import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from .public.css import *
import os

markdown_text = open(os.getcwd() + './data/home/markdown_files/introduction.txt', encoding='utf-8').read()
readme_text = open(os.getcwd() + './data/home/markdown_files/readme.txt', encoding='utf-8').read()
main_loop_text = open(os.getcwd() + './data/home/markdown_files/main loop.txt', encoding='utf-8').read()
editing_initialization_flow_text = open(os.getcwd() + './data/home/markdown_files/editing initialization flow.txt', encoding='utf-8').read()
editing_OSM_data_loading_text = open(os.getcwd() + './data/home/markdown_files/editing OSM data loading detailed process.txt', encoding='utf-8').read()
config_behavioral_file_text = open(os.getcwd() + './data/home/markdown_files/config behavioral file descriptions.txt', encoding='utf-8').read()
actions_and_behaviors_text = open(os.getcwd() + './data/home/markdown_files/actions and behaviors.txt', encoding='utf-8').read()


layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(children=[
                    html.Img(src=dash.get_asset_url('covid simulator.png'), style=style_front_img),
                ]),
                html.H3(style=style_title, id='datetime-text'),
                dcc.Interval(
                    id='datetime',
                    interval=20 * 1000,
                    n_intervals=0
                ),
                dcc.Markdown(style=style_mkd, children=markdown_text),
                html.Span('Details', className="badge bg-dark", style=style_badge),
                html.Div(style=style_wiki, children=[
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    dcc.Markdown(style=style_mkd, children=config_behavioral_file_text),
                                ],
                                title="Action and Behaviors"
                            ),
                            dbc.AccordionItem(
                                [
                                    dcc.Markdown(style=style_mkd, children=actions_and_behaviors_text),
                                ],
                                title="Config Behavioral File Descriptions"
                            ),
                            dbc.AccordionItem(
                                [
                                    dcc.Markdown(style=style_mkd, children=editing_initialization_flow_text),
                                ],
                                title="Initialization Flow"
                            ),
                            dbc.AccordionItem(
                                [
                                    dcc.Markdown(style=style_mkd, children=main_loop_text),
                                ],
                                title="Main Loop"
                            ),
                            dbc.AccordionItem(
                                [
                                    dcc.Markdown(style=style_mkd, children=editing_OSM_data_loading_text),
                                ],
                                title="OSM Data Loading Detailed Process"
                            ),
                        ]
                    )
                ]),
                html.Span('All Available Links', className="badge bg-dark", style=style_badge),
                html.Div(style=style_button, children=[
                    dbc.Button("About", color="primary", className="me-1", href="/about"),
                    dbc.Button("Configuration", color="dark", className="me-1", href="/configuration"),
                    dbc.Button("Map", color="dark", className="me-1", href="/map"),
                    dbc.Button("Log Result", color="info", className="me-1", href="/result"),
                    dbc.Button("Infection", color="info", className="me-1", href="/infection"),
                    dbc.Button("Evacuation", color="info", className="me-1", href="/evacuation"),
                    dbc.Button("Geographical", color="info", className="me-1", href="/geographical"),
                ]),
            ]
        )
    ]
)
dash.register_page(__name__, path='/')

