from dash import dcc, html, callback
from preprocess.helpers import read_figure
from dash.dependencies import Input, Output
import dash_daq as daq
from pathlib import Path
from preprocess.plot_4 import PreProcess

PP = PreProcess()
ABS_PATH = Path(__file__).parent.parent

GLOBAL_WARMING_DATA = ABS_PATH / "data/figs/plot_3/GlobalWarmingGraphs_1.json"
RANGE = range(1854, 2014, 10)


def layout():
    return html.Div(children=[
        html.H1('Change Ratio of Temperature Per Country',
                style={'textAlign': "center"}),
        daq.ToggleSwitch(
            id="toggle-box",
            value=False,
            label=["Box-plot", "Histogram"],
            color="#F96666",
            style={"color": "#black","float":"right",'display': 'inline-block'},
        ),
        dcc.Graph(id='change-ratio-graph',
                  figure=read_figure(ABS_PATH / "data/figs/plot_4/change_ratio_2004_24.json" ),
                  style={'display': 'inline-block', 'width': '100%', 'height': '800px',"automargin":"False"}
                  ),
        dcc.Slider(1854, 2014, 10, id='year_slider',value=1924, marks=None,
                   tooltip={"placement": "bottom", "always_visible": True}),
        dcc.Slider(1, 24, 1, id='limit-slider', value=12, marks=None,
                   tooltip={"placement": "bottom", "always_visible": True})

    ])


@callback(
    output=[Output("change-ratio-graph", "figure"),
            Output('limit-slider','step'),
            Output('limit-slider','min')],
    inputs=[Input("year_slider", "value"),
            Input("limit-slider", "value"),
            Input('toggle-box',"value")])
def update_graph(year,limit,box):
    if not box:
        return read_figure(ABS_PATH / f"data/figs/plot_4/change_ratio_box_{year}.json"),0,1804
    else:
        return read_figure(ABS_PATH / f"data/figs/plot_4/change_ratio_{year}_{limit}.json"),1,1854


