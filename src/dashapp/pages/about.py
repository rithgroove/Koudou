import dash
from dash import html, dcc, callback, Input, Output

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

dash.register_page(__name__, path='/about')

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3("   "),
                html.Img(src=dash.get_asset_url('mi1.png'), style=style_img),
                html.Img(src=dash.get_asset_url('mi2.png'), style=style_img),
                html.Img(src=dash.get_asset_url('mi3.png'), style=style_img),
            ]
        ),

    ]
)