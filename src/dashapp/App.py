from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
from pages.public.data import *
from pages.public.css import *

markdown_text = open('data/home/markdown_files/introduction.txt', encoding='utf-8').read()

app = Dash(__name__, use_pages=True, external_stylesheets=[BS])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("General", href="/config"),
                dbc.DropdownMenuItem("Map", href="/map"),
            ],
            nav=True,
            in_navbar=True,
            label="Configuration",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Simulation Log", href="/result"),
                dbc.DropdownMenuItem("Infection", href="/infection"),
                dbc.DropdownMenuItem("Evacuation", href="/evacuation"),
                dbc.DropdownMenuItem("Location", href="/geographical"),
            ],
            nav=True,
            in_navbar=True,
            label="Simulation Analysis",
        ),
        dbc.NavItem(dbc.NavLink("Model Verification", href="/verification")),
        dbc.NavItem(dbc.NavLink("Upload", href="/upload")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Introduction", href="/comparison_intro"),
                dbc.DropdownMenuItem("Infection", href="/comparison_infection"),
                dbc.DropdownMenuItem("Evacuation", href="/comparison_evacuation"),
                dbc.DropdownMenuItem("Geographical", href="/comparison_geo"),
                dbc.DropdownMenuItem("Log", href="/comparison_log"),
            ],
            nav=True,
            in_navbar=True,
            label="Comparison",
        ),
    ],
    brand="Simulator Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
)

navIncluded = html.Div(
    [
        dbc.Row(
            dbc.Col(html.Div([navbar])),
        )
    ]
)

app.layout = html.Div([
    navIncluded, dash.page_container,
    ]
)


if __name__ == '__main__':
	app.run_server(debug=True)
