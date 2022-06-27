from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from preprocess.plot_1 import PreProcess
from preprocess.helpers import read_figure
import os
import sys
from pathlib import Path
import dash_daq as daq

ABS_PATH = Path(__file__).parent.parent

CLIMATE_DATA = ABS_PATH / "data/CliamteChange/GroupByYear.csv"
FIG_PATH = ABS_PATH / "data/figs/plot_1"
YEARS_RANGE = range(1950, 2014)

pre_process_figs = {
    "_".join(p.split(".")[0].split("_")[1:]): read_figure(FIG_PATH/"agg"/f"{p}") for p in os.listdir(FIG_PATH / "agg")
}
# years_fig = {
#     int(p.split(".")[0].split("_")[-1]): read_figure(FIG_PATH/"years"/f"{p}") for p in os.listdir(FIG_PATH / "years")
# }

LAST_YEAR = None


def layout():
    return html.Div(children=[
        html.H1('Climate Change',
                style={'textAlign':"center"}),
        dcc.Dropdown(
            id='temp_dropdown',
            options=[
                {'label': 'Min Temperature', 'value': 'min_temp'},
                {'label': 'Avg Temperature', 'value': 'mean_temp'},
                {'label': 'Max Temperature', 'value': 'max_temp'},
            ],
            value='mean_temp',
            style={"width": "50%"}),
        dcc.Dropdown(
            id='year_dropdown',
            options=[{'label': year, 'value': year} for year in YEARS_RANGE],
            value=None,
            style={'display': 'inline-block',"width": "50%"}),
        dcc.Graph(id='climate-change-graph',
                  figure=pre_process_figs['mean_temp'],
                  style={'display': 'inline-block', 'width': '100%', 'height': '800px'}
                  )
    ])


@callback(
    output=Output("climate-change-graph", "figure"),
    inputs=[Input("temp_dropdown", "value"),
            Input("year_dropdown", "value")])
def update_graph(temp_mode, year):
    global LAST_YEAR
    if year is not None and year != 'None':
        if year == LAST_YEAR:
            return pre_process_figs[temp_mode]
        LAST_YEAR = year
        return read_figure(ABS_PATH / f"data/figs/plot_1/years/climate_year_{year}.json")
    else:
        return pre_process_figs[temp_mode]


