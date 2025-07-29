from functools import partial
import pandas as pd
import numpy as np
from universal_timeseries_transformer import map_timeserieses_to_list_of_timeserieses
from timeseries_performance_calculator.tables import (
    get_table_annualized_return_cagr,
    get_table_annualized_return_days,
    get_table_annualized_volatility,
    get_table_maxdrawdown,
    get_table_sharpe_ratio,
    get_table_beta_by_index,
    get_table_winning_ratio_by_index
)

def get_cross_sectional_performance_by_kernel(kernel, cross_sectional_prices, option_dropna=True):
    if option_dropna:
        cross_sectional_prices = cross_sectional_prices.dropna(axis=1, how='all')
    list_of_prices = map_timeserieses_to_list_of_timeserieses(cross_sectional_prices)
    dfs = [kernel(price.dropna()) for price in list_of_prices]
    df = pd.concat(dfs)
    return df

def get_cross_sectional_benchmark_performance_by_kernel(kernel, cross_sectional_prices, benchmark_price, option_dropna=True):
    if option_dropna:
        cross_sectional_prices = cross_sectional_prices.dropna(axis=1, how='all')
    list_of_prices = map_timeserieses_to_list_of_timeserieses(cross_sectional_prices)
    results = []
    for prices in list_of_prices:
        prices = prices.join(benchmark_price, how='left', rsuffix='_benchmark')
        df = kernel(prices)
        result = df.copy().iloc[:1, :]
        if '_benchmark' in df.index[-1]:
            result.iloc[0, 0] = np.nan
        results.append(result)
    return pd.concat(results)

get_cross_sectional_annualized_return_cagr = partial(get_cross_sectional_performance_by_kernel, get_table_annualized_return_cagr)
get_cross_sectional_annualized_return_days = partial(get_cross_sectional_performance_by_kernel, get_table_annualized_return_days)
get_cross_sectional_annualized_volatility = partial(get_cross_sectional_performance_by_kernel, get_table_annualized_volatility)
get_cross_sectional_maxdrawdown = partial(get_cross_sectional_performance_by_kernel, get_table_maxdrawdown)
get_cross_sectional_sharpe_ratio = partial(get_cross_sectional_performance_by_kernel, get_table_sharpe_ratio)
get_cross_sectional_beta_by_benchmark = partial(get_cross_sectional_benchmark_performance_by_kernel, get_table_beta_by_index)
get_cross_sectional_winning_ratio_by_benchmark = partial(get_cross_sectional_benchmark_performance_by_kernel, get_table_winning_ratio_by_index)

def get_cross_sectional_performances(cross_sectional_prices, benchmark_column_index=1, benchmark_price=None, option_dropna=True):
    if option_dropna:
        cross_sectional_prices = cross_sectional_prices.dropna(axis=1, how='all')
    df_annualized_return_cagr = get_cross_sectional_annualized_return_cagr(cross_sectional_prices, option_dropna=False)
    df_annualized_return_days = get_cross_sectional_annualized_return_days(cross_sectional_prices, option_dropna=False)
    df_annualized_volatility = get_cross_sectional_annualized_volatility(cross_sectional_prices, option_dropna=False)
    df_maxdrawdown = get_cross_sectional_maxdrawdown(cross_sectional_prices, option_dropna=False)
    df_sharpe_ratio = get_cross_sectional_sharpe_ratio(cross_sectional_prices, option_dropna=False)
    dfs = [df_annualized_return_cagr, df_annualized_return_days, df_annualized_volatility, df_maxdrawdown, df_sharpe_ratio]
    
    if benchmark_column_index is not None and benchmark_price is None:
        benchmark_price = cross_sectional_prices.iloc[:, benchmark_column_index]

    if benchmark_price is not None:
        df_beta_by_benchmark = get_cross_sectional_beta_by_benchmark(cross_sectional_prices, benchmark_price, option_dropna=False)
        df_winning_ratio_by_benchmark = get_cross_sectional_winning_ratio_by_benchmark(cross_sectional_prices, benchmark_price, option_dropna=False)
        dfs = [*dfs, df_beta_by_benchmark, df_winning_ratio_by_benchmark]
    return pd.concat(dfs, axis=1)
