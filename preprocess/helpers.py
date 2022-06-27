import json
from plotly.graph_objs.graph_objs import Figure
import plotly.io as pio
from preprocess.plot_1 import PreProcess
from tqdm import tqdm
from pathlib import Path


def save_figure(fig_dict, path, name):
    for k in tqdm(fig_dict):
        fig = fig_dict[k]
        new_name = f"{name}_{k}.json"
        if isinstance(path, Path):
            fig_path = path / new_name
        else:
            fig_path = path + "/" + new_name
        with open(fig_path, 'w') as f:
            pio.write_json(fig, f)


def read_figure(path):
    with open(path, 'r') as f:
        return pio.read_json(f)


def delete_figures(path):
    pass


def create_years_figs(CLIMATE_DATA, YEARS_RANGE):
    dic = {
        year: PreProcess().create_figure(CLIMATE_DATA, 'avg_temp', year) for year in YEARS_RANGE
    }
    save_figure(dic, "/Users/itayd/PycharmProjects/VisualizationProject/data/figs/plot_1/years", "climate_year")


if __name__ == '__main__':
    pp=PreProcess()
    ABS_PATH = Path(__file__).parent.parent

    CLIMATE_DATA = ABS_PATH / "data/CliamteChange/GroupByYear.csv"

    create_years_figs(CLIMATE_DATA,range(1950,2013))
