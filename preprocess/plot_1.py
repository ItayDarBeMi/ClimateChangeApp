from typing import Union
from tqdm import tqdm
import pandas as pd
import plotly.express as px
from pathlib import Path


class PreProcess:

    def __init__(self):
        self.abs_path = Path(__file__).parent.parent
        self.df = pd.read_csv(
            self.abs_path / "data/CliamteChange/GlobalLandTemperaturesByCountry.csv"
        )
        self.countries = pd.read_csv(
            self.abs_path / "data/wikipedia-iso-country-codes.csv").rename(
            columns={'English short name lower case': "Country"})
        self.temp_df = self.df.dropna(subset=["AverageTemperature"]).merge(self.countries, how='left', on="Country")
        self.names_dic = {}

    @staticmethod
    def handle_missing_names(temp_df, countries):
        Stop_words = ["Republic", "Island", "And", "Islands"]
        dic = {
            name: {
                c: 0 for c in countries.Country
            } for name in temp_df[temp_df['Alpha-2 code'].isnull()]['Country'].unique()}
        for name in temp_df[temp_df['Alpha-2 code'].isnull()]['Country'].unique():
            for c in countries.Country:
                split_name = name.split(" ")
                for part_name in split_name:
                    if part_name in Stop_words:
                        continue
                    if part_name in c.split(" "):
                        # print(f"{name} | {part_name} | {c} = True")
                        dic[name][c] += 1

        new_dic = {}
        for k in dic:
            rate = [i for i in sorted(dic[k].items(), key=lambda x: x[1], reverse=True) if i[1] > 0]
            # print(f"{k} -> {rate}")
            new_dic[k] = rate[0][0] if (len(rate) > 0) else None

        new_dic['Netherlands (Europe)'] = 'Netherlands'
        new_dic['Africa'] = None

        return new_dic

    def modified_country(self, country):
        if country in self.names_dic:
            return self.names_dic[country]
        else:
            return country

    def prepare_data_for_figure(self):
        self.df['Country'] = self.df['Country'].apply(self.modified_country)
        df = self.df.dropna(subset=["AverageTemperature"]).merge(self.countries, how='left', on="Country").dropna(
            subset=["Country"])
        df['year'] = df['dt'].apply(lambda x: x.split("-")[0])
        gr = df.groupby(["Country", "year"])
        gr_agg = gr.agg({"AverageTemperature": ["mean", "min", "max"]})
        new_df = {
            "Country": [],
            "avg_temp": [],
            "max_temp": [],
            "min_temp": [],
            "year": []
        }

        for k in tqdm(gr.groups):
            new_df["Country"].append(k[0])
            new_df["year"].append(k[1])

        for i in tqdm(range(gr_agg.shape[0])):
            new_df["avg_temp"].append(gr_agg.iloc[i]['AverageTemperature']['mean'])
            new_df["max_temp"].append(gr_agg.iloc[i]['AverageTemperature']['max'])
            new_df["min_temp"].append(gr_agg.iloc[i]['AverageTemperature']['min'])

        return pd.DataFrame(new_df).merge(self.countries, how='inner', on='Country').sort_values("year")

    @staticmethod
    def create_figure(data: Union[pd.DataFrame, str, Path], color='avg_temp', year=None):
        if isinstance(data, (str, Path)):
            data = pd.read_csv(data)
        fig_conf = dict(locations="Country",
                        color=color,
                        hover_name="Country",
                        locationmode='country names',
                        color_continuous_scale='RdYlBu_r'
                        )
        layout_conf = dict(geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            resolution=110,
            visible=True
        )
        )
        if year is not None and (year in data.year.unique()):
            data = data[data.year == year]
            layout_conf['title_text'] = f'World Climate Change - {year}'
        else:
            fig_conf['animation_frame'] = 'year'
            layout_conf['title_text'] = f'World Climate Change - Animation'
        fig = px.choropleth(data_frame=data, **fig_conf)
        fig.update_layout(**layout_conf)
        try:
            fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 0.01
            fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0.01
        except IndexError:
            pass
        return fig


if __name__ == '__main__':
    pp = PreProcess()

    ABS_PATH = Path(__file__).parent.parent

    CLIMATE_DATA = ABS_PATH / "data/CliamteChange/GroupByYear.csv"
