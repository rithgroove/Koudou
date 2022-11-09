import dash
from dash import html, dcc, callback, Input, Output

style_title = {
    'textAlign': 'center',
    'marginLeft': '100px',
    'marginRight': '100px'
}

style_markdown = {
    'margin-left': '250px'
}

markdown_text = open('data/markdown_text_demo', encoding='utf-8').read()

dash.register_page(__name__)

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2(style=style_title, children="Dashboard Introduction"),
                html.H3(style=style_title, id='datetime-text'),
                dcc.Interval(
                    id='datetime',
                    interval=20 * 1000,
                    n_intervals=0
                ),
                html.Div(style=style_markdown, children=[
                    html.Img(src='https://askabiologist.asu.edu/sites/default/files/headers/covidsim-header_0.png', alt="Model Introduction Picture"),
                    dcc.Markdown(children=markdown_text),
                ])

            ]
        ),

    ]
)