import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import colorlover as cl
from plotly.subplots import make_subplots
from preprocess.helpers import save_figure

ABSPATH = Path(__file__).parent.parent

data = pd.read_csv(ABSPATH / "data/CliamteChange/GlobalTemperatures.csv")

data.dropna(axis=0, inplace=True)

# Dealing with the DATE
data['Date'] = pd.to_datetime(data.dt)  # converted all dates to the same format

data2 = data.copy()  # create a new dataset
data2.drop(columns=['dt'], axis=1, inplace=True)  # drop the dt column

# Creating new features
data2['day'] = data2['Date'].dt.day
data2['week'] = data2['Date'].dt.week
data2['month'] = data2['Date'].dt.month
data2['year'] = data2['Date'].dt.year

# Week data is not evenly distributed
data2['week'].value_counts()  # very uneven information on weeks

# For future analysis, we will work only on yearly data, as average (because there are dates missing and data is not consistent)
EARTH_DATA = data2.groupby(by='year')[['LandAverageTemperature', 'LandAverageTemperatureUncertainty',
                                       'LandMaxTemperature', 'LandMaxTemperatureUncertainty',
                                       'LandMinTemperature', 'LandMinTemperatureUncertainty',
                                       'LandAndOceanAverageTemperature',
                                       'LandAndOceanAverageTemperatureUncertainty']].mean().reset_index()

EARTH_DATA['turnpoint'] = np.where(EARTH_DATA['year'] <= 1975, 'before', 'after')  # creating a new columns


def layout():
    fig = make_subplots(rows=2, cols=2, insets=[{'cell': (1, 1), 'l': 0.7, 'b': 0.3}])
    fig.update_layout(title="When Global Warming Started?",
                      font=dict(family="Courier New, monospace", size=12, color="#7f7f7f"),
                      template="ggplot2", title_font_size=20, hovermode='closest')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='gray')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='gray')

    # Figure data
    fig.add_trace(go.Scatter(x=EARTH_DATA['year'], y=EARTH_DATA['LandAverageTemperature'], mode='lines',
                             name='Land Avg Temp', marker_color='green'), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=[1975, 1975], y=[7.5, 10], mode="lines", line=go.scatter.Line(color="gray"), showlegend=False),
        row=1, col=1)

    fig.add_trace(go.Scatter(x=EARTH_DATA['year'], y=EARTH_DATA['LandMinTemperature'], mode='lines',
                             name='Land Min Temp', marker_color='rgb(135,206,235)'), row=1, col=2)
    fig.add_trace(
        go.Scatter(x=[1975, 1975], y=[1.5, 4.5], mode="lines", line=go.scatter.Line(color="gray"), showlegend=False),
        row=1, col=2)

    fig.add_trace(go.Scatter(x=EARTH_DATA['year'], y=EARTH_DATA['LandMaxTemperature'], mode='lines',
                             name='Land Max Temp', marker_color='red'), row=2, col=1)
    fig.add_trace(
        go.Scatter(x=[1975, 1975], y=[13, 15.5], mode="lines", line=go.scatter.Line(color="gray"), showlegend=False),
        row=2, col=1)

    fig.add_trace(go.Scatter(x=EARTH_DATA['year'], y=EARTH_DATA['LandAndOceanAverageTemperature'], mode='lines',
                             name='Land&Ocean Avg Temp', marker_color='blue'), row=2, col=2)
    fig.add_trace(
        go.Scatter(x=[1975, 1975], y=[14.5, 16], mode="lines", line=go.scatter.Line(color="gray"), showlegend=False),
        row=2, col=2)
    return fig


if __name__ == '__main__':
    figure = layout()
    save_figure({1:figure}, ABSPATH / "data/figs/plot_3", "GlobalWarmingGraphs")
