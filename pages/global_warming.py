from dash import dcc, html
import dash_bootstrap_components as dbc
from preprocess.helpers import read_figure
from pathlib import Path

ABS_PATH = Path(__file__).parent.parent

GLOBAL_WARMING_DATA = ABS_PATH / "data/figs/plot_3/GlobalWarmingGraphs_1.json"


def layout():
    return html.Div(children=[
        html.H1('Global Warming - 4 Graphs That Pointing to One future',
                style={'textAlign': "center"}),
        dcc.Graph(id='global-warming-graph',
                  figure=read_figure(GLOBAL_WARMING_DATA),
                  style={'display': 'inline-block', 'width': '100%', 'height': '800px'}
                  )
    ])