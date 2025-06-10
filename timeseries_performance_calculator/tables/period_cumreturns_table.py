import pandas as pd
from typing import List, Tuple, TypeVar, Union
from itertools import starmap
from universal_timeseries_transformer import PricesMatrix
from canonical_transformer import map_number_to_signed_string
from timeseries_performance_calculator.dataframe_basis.dataframe_calculator import get_cumreturns_row_between_dates
from .consts import COLUMNS_DEFAULT_BENCHMARK_ORDERS, MAPPING_INDEX_NAMES

def get_period_cumreturns_table(timeseries: pd.DataFrame) -> pd.DataFrame:
    pm = PricesMatrix(timeseries)
    data_historical_dates = pm.historical_dates

    return pd.concat(
        starmap(lambda label, date: get_cumreturns_row_between_dates(pm.df, date_i=date, label_cumreturn=label), 
                data_historical_dates.items()), 
    axis=0
)
def reorder_benchmark_columns(
    df: pd.DataFrame, 
    columns_ordered: List[str] = COLUMNS_DEFAULT_BENCHMARK_ORDERS
) -> pd.DataFrame:

    def partition_by_membership(items: List[str], reference_set: set[str]) -> Tuple[List[str], List[str]]:
        members = [item for item in items if item in reference_set]
        non_members = [item for item in items if item not in reference_set]
        return members, non_members
    
    def order_by_reference(items: List[str], reference_order: List[str]) -> List[str]:
        return [item for item in reference_order if item in items]
    
    current_columns = list(df.columns)
    preferred_set = set(columns_ordered)
    
    _, non_preferred = partition_by_membership(current_columns, preferred_set)
    ordered_preferred = order_by_reference(current_columns, columns_ordered)
    
    return df[ordered_preferred + non_preferred]

def rename_first_column(df: pd.DataFrame, new_name: str = 'Fund') -> pd.DataFrame:
    df = df.copy()
    df.columns = [new_name] + list(df.columns[1:])
    return df

def rename_benchmark_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.rename(columns=MAPPING_INDEX_NAMES)
    return df

def transform_to_signed_numbers_with_percentage(df: pd.DataFrame, decimal_digits: int) -> pd.DataFrame:
    df = df.copy()
    df = df.map(lambda x: map_number_to_signed_string(x, decimal_digits=decimal_digits))
    df = df.map(lambda x: f'{x}%')
    return df

def reorder_benchmark_columns_simple(df: pd.DataFrame) -> pd.DataFrame:
    LEGACY_BENCHMARK_ORDER = ['Fund', 'KOSPI', 'KOSPI 200', 'KOSDAQ', 'S&P 500']
    if set(df.columns) == set(LEGACY_BENCHMARK_ORDER):
        return df[LEGACY_BENCHMARK_ORDER]
    return df

def show_period_cumreturns_table(
    prices: pd.DataFrame, 
    decimal_digits: Union[int, None] = None, 
    option_signed: bool = True
) -> pd.DataFrame:
    df = get_period_cumreturns_table(prices)
    df = rename_first_column(df)
    # df = reorder_benchmark_columns(df)
    df = rename_benchmark_columns(df)
    df = reorder_benchmark_columns_simple(df)
    df = transform_to_signed_numbers_with_percentage(df, decimal_digits) if option_signed else df
    return df
