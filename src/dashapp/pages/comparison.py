import dash
from dash import html

dash.register_page(__name__, path='/comparison_intro')

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3("   "),
            ]
        ),

    ]
)