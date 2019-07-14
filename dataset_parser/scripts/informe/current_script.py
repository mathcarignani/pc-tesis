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


test_results_to_pandas()

