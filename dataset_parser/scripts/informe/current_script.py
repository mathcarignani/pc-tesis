import sys
sys.path.append('.')

import pandas as pd

from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.results_parsing.results_reader import ResultsReader


def test_results_to_dataframe():
    results_reader = ResultsReader('global', 3)
    dataset_name = 'IRKIS'
    df = ResultsToDataframe(results_reader).create_dataframe(dataset_name, 'Global')
    PandasUtils(dataset_name, df, 3)


test_results_to_dataframe()

