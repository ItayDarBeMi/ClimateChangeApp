from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from preprocess.plot_2 import CreateData
from preprocess.helpers import read_figure
import os
from pathlib import Path
import dash_daq as daq

DATA = CreateData()
ABS_PATH = Path(__file__).parent.parent

FIG_PATH = ABS_PATH / "data/figs/plot_2"

# CLIMATE_DICT = {c: DATA.create_figure(DATA.lines_data, c) for c in DATA.conts}
MAX_COUNTRIES = 201
# LIMIT_DICT = {
#     c: {
#         int(p.split(".")[0].split("_")[-1]): read_figure(
#             path=FIG_PATH / "limit" / f"{c}_limit_{p.split('.')[0].split('_')[-1]}.json"
#         ) for p in
#         os.listdir(FIG_PATH / "limit") if c in p
#     }
#     for c in DATA.conts
# }

CONT_OPTIONS = [{'label': i, 'value': i} for i in DATA.conts]
# for c in LIMIT_DICT:
#     save_figure(LIMIT_DICT[c],
#                 "/Users/itayd/PycharmProjects/VisualizationProject/data/figs/plot_2/limit",
#                 f"{c}_limit")


def layout():
    return html.Div(children=[
        html.H1('Mean Country Temp Per Continent',
                style={'textAlign': "center"}),
        daq.ToggleSwitch(
            id="cold-toggle-map",
            value=True,
            label=["Coldest", "Hottest"],
            color="#F96666",
            style={"color": "#black","float":"right"},
        ),
        dcc.Dropdown(
            id='continent_dropdown',
            options=CONT_OPTIONS,
            value="Africa",
            style={"width": "40%"}),
        dcc.Dropdown(
            id='limit_dropdown',
            options=[{'label': i, 'value': i} for i in range(1, MAX_COUNTRIES)],
            value="1",
            style={"width": "40%"}),
        dcc.Graph(id='country-line-chart',
                  figure=read_figure(ABS_PATH / "data/figs/plot_2/limit/Europe_limit_5.json"),
                  style={'display': 'inline-block', 'width': '100%', 'height': '800px'}
                  )
    ])


@callback(
    Output("country-line-chart", "figure"),
    [Input("continent_dropdown", "value"),
     Input("limit_dropdown", "value"),
     Input("cold-toggle-map", "value")])
def update_line_chart(continent, limit,cold):
    ALL_FIGS = os.listdir(ABS_PATH / "data/figs/plot_2/limit")
    MAX_LIMIT = max([int(i.split(".")[0].split("_")[-1]) for i in ALL_FIGS
                     if i.split(".")[0].split("_")[0] == continent])
    if continent == 'all':
        return read_figure(ABS_PATH / f"data/figs/plot_2/limit/{continent}_limit_{limit}.json")
    if limit is None or limit > DATA.countries_pre_cont[continent]:
        limit = MAX_LIMIT
    else:
        if not cold:
            try:
                return read_figure(ABS_PATH / f"data/figs/plot_2/limit/{continent}_limit_cold_{limit}.json")
            except Exception as e:
                limit = MAX_LIMIT
    return read_figure(ABS_PATH / f"data/figs/plot_2/limit/{continent}_limit_{limit}.json")

