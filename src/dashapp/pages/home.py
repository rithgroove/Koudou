import dash
from dash import html, dcc, callback, Input, Output
import base64

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

markdown_text = open('data/home/markdown_files/introduction.txt', encoding='utf-8').read()
readme_text = open('data/home/markdown_files/readme.txt', encoding='utf-8').read()

dash.register_page(__name__, path='/')

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(style=style_img, children=[
                    # dcc.Markdown(children=markdown_text),
                    html.Img(src=dash.get_asset_url('covid simulator.png'), style=style_img),
                ]),
                html.H3(style=style_title, id='datetime-text'),
                dcc.Interval(
                    id='datetime',
                    interval=20 * 1000,
                    n_intervals=0
                ),
                dcc.Markdown(style=style_img, children=markdown_text)
                # dcc.Markdown(style=style_img, children=readme_text)
            ]
        ),

    ]
)