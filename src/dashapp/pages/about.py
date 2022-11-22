import dash
from dash import html

style_title = {
    'textAlign': 'center',
    'marginLeft': '100px',
    'marginRight': '100px',
}

style_dropdown = {
    'width': '250px'
}

dash.register_page(__name__)

layout = html.Div(style=style_title,
    children=[
        html.H5("This is about page")
    ]
)
