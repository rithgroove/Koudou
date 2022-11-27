import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

style_title = {
    'textAlign': 'center'
}

style_markdown = {
    'margin-left': '250px'
}

style_img = {
    'width': '60%',
    'marginLeft': '20%',
    'marginRight': '20%'
}

style_button = {
    'width': '80%',
    'marginLeft': '20%',
    'marginRight': '10%'
}

markdown_text = open('data/home/markdown_files/introduction.txt', encoding='utf-8').read()
readme_text = open('data/home/markdown_files/readme.txt', encoding='utf-8').read()

dash.register_page(__name__, path='/')

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(style=style_img, children=[
                    html.Img(src=dash.get_asset_url('covid simulator.png'), style=style_img),
                ]),
                html.H3(style=style_title, id='datetime-text'),
                dcc.Interval(
                    id='datetime',
                    interval=20 * 1000,
                    n_intervals=0
                ),
                dcc.Markdown(style=style_img, children=markdown_text),
                html.Br(),
                html.H3("All Available Links for Pages Above", style=style_title),
                html.Div(style=style_button, children=
                [
                    dbc.Button("About", color="primary", className="me-1", href="/about"),
                    dbc.Button("Configuration", color="dark", className="me-1", href="/configuration"),
                    dbc.Button("Map", color="dark", className="me-1", href="/map"),
                    dbc.Button("Log Result", color="info", className="me-1", href="/result"),
                    dbc.Button("Infection", color="info", className="me-1", href="/infection"),
                    dbc.Button("Evacuation", color="info", className="me-1", href="/evacuation"),
                    dbc.Button("Geographical", color="info", className="me-1", href="/geographical"),
                ]
                         ),
                # dcc.Markdown(style=style_img, children=readme_text)
            ]
        ),

    ]
)