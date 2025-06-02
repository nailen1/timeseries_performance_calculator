import pandas as pd
import numpy as np
from financial_dataset_preprocessor.preprocess_consts import RETURNS_PREFIX

def get_beta(df_returns_with_benchmark):
    if df_returns_with_benchmark.shape[1] != 2:
        raise ValueError("DataFrame must have exactly 2 columns")
    return_portfolio = df_returns_with_benchmark.iloc[:, 0]
    return_benchmark = df_returns_with_benchmark.iloc[:, 1]
    return np.cov(return_portfolio, return_benchmark)[0][1] / np.var(return_benchmark)

def get_data_beta(df_returns_with_benchmark):
    cols = df_returns_with_benchmark.columns
    name_portfolio, name_benchmark = [col.replace(RETURNS_PREFIX, '') for col in cols]
    beta = get_beta(df_returns_with_benchmark)
    dct = {'portfolio': name_portfolio, 'benchmark': name_benchmark, 'beta': beta}
    return dct

def get_beta_of_multi_timeseries(df_returns_with_benchmark, benchmark):
    lst = []
    cols = df_returns_with_benchmark.columns
    col_benchmark = [col for col in cols if benchmark in col][0]
    for col in df_returns_with_benchmark.columns:
        if col_benchmark not in col:
            df = df_returns_with_benchmark[[col, col_benchmark]]
            data_beta = get_data_beta(df)
            portfolio = data_beta['portfolio']
            beta = data_beta['beta']
            lst.append({'portfolio': portfolio, 'beta': beta})
        else:
            lst.append({'portfolio': benchmark, 'beta': '-'})
    df = pd.DataFrame(lst).set_index('portfolio').T
    df.columns.name = None
    return df
