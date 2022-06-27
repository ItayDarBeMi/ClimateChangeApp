from dash import Dash, Input, Output, dcc, html, page_container
import dash_bootstrap_components as dbc
from pages.climate_changes import layout as climate_layout
from pages.line_chart_per_country import layout as line_chart_layout
from pages.global_warming import layout as global_warming_layout
from pages.change_ratio import layout as change_ration_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        html.H2("Climate.io", className="display-4"),
        html.Hr(),
        html.P(
            "A simple App for visualizing climate changes", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Climate Change Over Time (Map)", href="/climate-changes-map", active="exact"),
                dbc.NavLink("Climate Change Over Time (Line)", href="/climate-changes-line", active="exact"),
                dbc.NavLink("Global Warming", href="/global-warming", active="exact"),
                dbc.NavLink("Change Ratio", href="/change-ratio", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        page_container
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/climate-changes-map" or pathname == "/":
        return climate_layout()
    elif pathname == "/climate-changes-line":
        return line_chart_layout()
    elif pathname == "/global-warming":
        return global_warming_layout()
    elif pathname == "/change-ratio":
        return change_ration_layout()
    return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == '__main__':
    app.run_server(debug=True)

