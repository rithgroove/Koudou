from dash import Dash, html, dcc
import dash

style_title = {
    'textAlign': 'center',
    'marginLeft': '100px',
    'marginRight': '100px'
}

style_navLink={
    'textAlign': 'center',
}

style_title = {
    'textAlign': 'center',
    'marginLeft': '100px',
    'marginRight': '100px'
}

style_markdown = {
    'margin-left': '250px'
}


markdown_text = open('data/markdown_text_demo', encoding='utf-8').read()

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
	html.H1('Modular Small Community Simulator Dashboard Demo', style=style_title),

    html.Div(style=style_navLink, children=[
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
	dash.page_container,
])

if __name__ == '__main__':
	app.run_server(debug=True)
