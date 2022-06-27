import pandas as pd
import plotly.express as px
from pathlib import Path
from tqdm import tqdm
from preprocess.helpers import save_figure


class PreProcess:

    def __init__(self):
        self.abs_path = Path(__file__).parent.parent
        self.df = pd.read_csv(
            self.abs_path / "data/line_chart_data.csv"
        )
        self.continents = pd.read_csv(
            self.abs_path / "data/continents2.csv").rename(columns={"name": "country"})

    def prepare_data(self, year):
        cnrts = self.df.country.unique()
        dic = {c: 0 for c in cnrts}
        for country in cnrts:
            dic[country] = self.df[(self.df.country == country) & (self.df.year > year)].dropna(
                subset=['yearly_mean']
            )['yearly_mean'].pct_change()
        mean_heat = {c: dic[c].mean() * 100 for c in dic}
        mean_heat = sorted(mean_heat.items(), key=lambda x: x[1], reverse=True)
        new_df = pd.DataFrame(mean_heat)
        new_df = new_df.rename(columns={0: "country", 1: "mean"}).merge(
            self.continents[['country', 'region']].drop_duplicates(subset=['country']), how='left',
            on='country').dropna()
        new_df['mean'] = new_df['mean'].apply(lambda x: x if x < 10 else 10)
        new_df['mean'] = new_df['mean'].apply(lambda x: x if x > -10 else -10)
        return new_df

    def create_hist(self, df=None):
        if df is not None:
            return px.histogram(df, y="mean", facet_col="region", color="country")
        else:
            return px.histogram(df, y="mean", facet_col="region", color="country")

    def create_box(self, df):
        return px.box(df, y="mean", color="region", points="all", hover_name='country')


if __name__ == '__main__':
    pp = PreProcess()
    dic = {}
    try:
        for year in tqdm(range(1804, 2023, 5)):
            df = pp.prepare_data(year)
            dic[f"box_{year}"] = pp.create_box(df)
    except Exception as e:
        pass
    save_figure(dic, pp.abs_path / "data/figs/plot_4", name="change_ratio")
