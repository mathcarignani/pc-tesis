import sys
sys.path.append('.')

import pandas as pd

from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.results_parsing.results_to_pandas import ResultsToPandas
from scripts.informe.results_parsing.results_reader import ResultsReader


def test_results_to_pandas():
    results_reader = ResultsReader('global', 3)
    dataset_name = 'IRKIS'
    df = ResultsToPandas(results_reader).create_dataframe(dataset_name, 'Global')

    PandasUtils(dataset_name, df)

    basic_coder_total = df.loc[df['coder'] == "CoderBasic"]['column_1'].iloc[0]
    df['new'] = 100 * (df['column_1'] / basic_coder_total)
    # print df


test_results_to_pandas()

