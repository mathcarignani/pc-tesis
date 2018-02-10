import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class NOAAUtils:
    NAME = "NOAA"

    def __init__(self):
        pass

    # @classmethod
    # def map_value(cls, value):
    #     return round(float(value)*1000, 0)

    @classmethod
    def plot(cls, filename, df):
        title = filename
        df = df.copy(deep=True)
        min_value = df.loc[df.idxmin()]['SST'][0]
        max_value = df.loc[df.idxmax()]['SST'][0]
        df['SSTnan'] = df['SST']
        nan_value = min_value - (max_value - min_value) / 10
        df['SSTnan'] = df['SSTnan'].apply(lambda x: nan_value if pd.isnull(x) else np.nan)

        fig, ax = plt.subplots()
        df['SST'].plot(ax=ax, linestyle='none', title=title, marker='.', markersize=0.2)
        df['SSTnan'].plot(ax=ax, linestyle='none', marker='.', markersize=1)
        ax.legend()
        fig = ax.get_figure()
        fig.savefig(title + '.plot.png')
