import dash
from dash import html
from .public.css import *

dash.register_page(__name__)

layout = html.Div(style=style_title,
    children=[
        html.H5("This is Map Analysis page")
    ]
)
