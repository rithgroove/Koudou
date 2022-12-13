import dash
from dash import dcc, html, callback, State, Input, Output
from .public.css import *
from dash.dependencies import Input, Output, State
from .public.utils import *
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div([
    html.Br(),
    html.Div(style=style_offcanvas, children=[
        dbc.Button("Instructions", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            html.P(
                "In this module, you can upload up to three model result sets, the results will be shown in the"
                " comparison module. Based on the analytical components developed in the simulation analysis module,"
                "we will review and compare they based on the data you upload."
            ),
            id="offcanvas",
            title="How Upload Works",
            is_open=False,
        ),
    ]),
    html.Br(),
    html.Div("Upload Model One", style=style_title),
    dcc.Upload(
        id='upload-data-first-model',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style=style_upload_bottom,
        # Allow multiple files to be uploaded
        multiple=True
    ),
    # html.Div(style=style_upload_csv_show, id='output-data-upload'),
    html.Br(),
    html.Div("Upload Model Two", style=style_title),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style=style_upload_bottom,
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Br(),
    html.Div("Upload Model Three", style=style_title),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style=style_upload_bottom,
        # Allow multiple files to be uploaded
        multiple=True
    ),
])

@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(Output('output-data-upload', 'children'),
              Input('upload-data-first-model', 'contents'),
              State('upload-data-first-model', 'filename'),
              State('upload-data-first-model', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


