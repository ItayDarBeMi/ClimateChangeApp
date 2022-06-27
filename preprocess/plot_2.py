from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from preprocess.helpers import save_figure
from pathlib import Path


class CreateData:

    def __init__(self):
        self.abs_path = Path(__file__).parent.parent
        self.lines_data = pd.read_csv(self.abs_path / "data/line_chart_data.csv")
        self.noc = pd.read_csv(self.abs_path / "data/noc_regions.csv").rename(
            columns={'region': "country"})
        self.continents = pd.read_csv(self.abs_path / "data/continents2.csv").rename(
            columns={"name": "country", "region": "continent"}
        )[['country', 'continent']].drop_duplicates(subset=['country'])
        self.lines_data = self.lines_data.merge(self.noc, how='left', on='country')
        self.lines_data = self.lines_data.merge(self.continents,
                                                how="left",
                                                on="country"
                                                ).dropna(subset=["continent"])
        self.conts = list(self.lines_data.dropna(subset=['continent'])['continent'].unique()) + ['all']
        self.lenghts = {c: self.lines_data[self.lines_data['continent'] == c].shape[0] for c in self.conts}
        self.hottest, self.all_sorted = self.get_country_by_heat_rate()
        self.coldest = {c: self.hottest[c][::-1] for c in self.hottest}
        self.countries_pre_cont = {c: self.lines_data[self.lines_data['continent'] == c]['country'].unique().shape[0]
                                   for c in self.conts}

    def _get_data(self):
        return self.lines_data

    @property
    def data(self):
        return self._get_data

    def create_figure(self, data, continent: str = None, limit=None,hottest=True):
        new_data = data.copy()
        if continent is not None:
            if limit is not None:
                if hottest:
                    countries = self.hottest[continent][:limit]
                    new_data = new_data[(new_data['continent'] == continent) & (new_data['country'].isin(countries))]
                else:
                    countries = self.coldest[continent][:limit]
                    new_data = new_data[(new_data['continent'] == continent) & (new_data['country'].isin(countries))]
            else:
                new_data = new_data[new_data['continent'] == continent]
        else:
            if limit is not None:
                countries = self.all_sorted[:limit]
                new_data = new_data[new_data['country'].isin(countries)]
        fig = px.line(new_data, x='year', y='yearly_mean', color='country', markers=True)
        return fig

    def get_country_by_heat_rate(self):
        dic = {}
        all_sorted = []
        for c in self.lines_data['continent'].unique():
            c_df = self.lines_data[self.lines_data['continent'] == c]
            c_df = c_df.groupby("country").agg({
                "yearly_mean": ["mean"]
            }).sort_values(by=("yearly_mean", "mean"), ascending=False)
            dic[c] = [(i[0]) for i in c_df.iterrows()]
            all_sorted += [(i[0], i[1][0]) for i in c_df.iterrows()]
        all_sorted = sorted(all_sorted, key=lambda x: x[1], reverse=True)
        return dic, [c[0] for c in all_sorted]


if __name__ == '__main__':
    create = CreateData()
    # create.create_figure(create.lines_data).show()
    # save_figure(
    #     fig_dict={i: create.create_figure(create.lines_data, limit=i) for i in
    #               range(1, sum([val for val in create.countries_pre_cont.values()]))},
    #     path="/Users/itayd/PycharmProjects/VisualizationProject/data/figs/plot_2/limit",
    #     name="all_limit"
    # )
    for c in create.conts:
        save_figure(
            fig_dict={
                i: create.create_figure(create.lines_data,continent=c, limit=i,hottest=False)
                for i in range(1, create.countries_pre_cont[c])
            },
            path=create.abs_path / "data/figs/plot_2/limit",
            name=f"{c}_limit_cold"
        )
