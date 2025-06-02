from functools import partial
from typing import Callable, Any
import pandas as pd
from universal_timeseries_transformer import TimeseriesMatrix
from string_date_controller import get_date_n_months_ago, get_date_n_years_ago, get_first_date_of_year, get_last_date_of_month

def calculate_cumreturn_percentage(start_value: float, end_value: float) -> float:
    return (end_value / start_value - 1) * 100

def get_date_range_data(pm: Any, start_date: str, end_date: str) -> pd.DataFrame:
    return pm.rows_by_names(names=[start_date, end_date])

def add_cumreturn_row(data: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    result = data.copy()
    result.loc['cumreturn', :] = data.apply(
        lambda col: calculate_cumreturn_percentage(col[start_date], col[end_date]), 
        axis=0
    )
    return result

def rename_index_name(df, new_index_name):
    df = df.rename_axis(new_index_name)
    return df

def apply_index_name(data: pd.DataFrame, index_name: str) -> pd.DataFrame:
    return rename_index_name(data, new_index_name=index_name)

def create_cumreturn_system_with_n(
    date_calculator: Callable[[Any, int], str],
    index_name_formatter: Callable[[int], str]
) -> Callable[[Any, int], pd.DataFrame]:
    def cumreturn_system(prices: Any, n: int) -> pd.DataFrame:
        pm = TimeseriesMatrix(prices)
        date_f = pm.date_f
        start_date = date_calculator(pm, n)
        
        return (prices
                .pipe(lambda p: TimeseriesMatrix(p))
                .pipe(lambda pm: get_date_range_data(pm, start_date, date_f))
                .pipe(lambda data: add_cumreturn_row(data, start_date, date_f))
                .pipe(lambda data: apply_index_name(data, index_name_formatter(n)))
                )

    
    return cumreturn_system

def create_cumreturn_system_simple(
    date_calculator: Callable[[Any], str],
    index_name: str
) -> Callable[[Any], pd.DataFrame]:
    def cumreturn_system(prices: Any) -> pd.DataFrame:
        pm = TimeseriesMatrix(prices)
        date_f = pm.date_f
        start_date = date_calculator(pm)
        
        return (prices
                .pipe(lambda p: TimeseriesMatrix(p))
                .pipe(lambda pm: get_date_range_data(pm, start_date, date_f))
                .pipe(lambda data: add_cumreturn_row(data, start_date, date_f))
                .pipe(lambda data: apply_index_name(data, index_name)))
    
    return cumreturn_system

def get_n_months_ago_last_date(pm: Any, n: int) -> str:
    return get_last_date_of_month(get_date_n_months_ago(pm.date_f, n))

def get_n_years_ago_last_date(pm: Any, n: int) -> str:
    return get_last_date_of_month(get_date_n_years_ago(pm.date_f, n))

def get_year_first_date_simple(pm: Any) -> str:
    return get_first_date_of_year(pm.date_f)

def get_inception_date_simple(pm: Any) -> str:
    return pm.date_i

get_info_system_n_month_cumreturn = create_cumreturn_system_with_n(
    get_n_months_ago_last_date,
    lambda n: f'{n}month'
)

get_info_system_n_year_cumreturn = create_cumreturn_system_with_n(
    get_n_years_ago_last_date,
    lambda n: f'{n}year'
)

get_info_system_ytd_cumreturn = create_cumreturn_system_simple(
    get_year_first_date_simple,
    'YTD'
)

get_info_system_inception_cumreturn = create_cumreturn_system_simple(
    get_inception_date_simple,
    'inception'
)