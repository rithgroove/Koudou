import dash
from dash import dcc, html, callback, State, Input, Output
from .public.css import *
from dash.dependencies import Input, Output, State
from .public.utils import *
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div([
    html.Div(style=style_offcanvas, children=[
        dbc.Button("Instructions", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            html.P(
                "In this module, you can upload you own result files that from the simulation result"
                " with file names as follows: "
                "activity_history, agent_position_summary, disease_transition, evacuation, infection_summary, "
                "infection_transition, new_infection. The analysis content will be updated automatically based on "
                "the uploaded files. "
            ),
            id="offcanvas",
            title="How Upload Works",
            is_open=False,
        ),
    ]),
    # html.Div("Upload infection_summary.csv", style=style_title),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style=style_upload_bottom,
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(style=style_upload_csv_show, id='output-data-upload'),
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
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


