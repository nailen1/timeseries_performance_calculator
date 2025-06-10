import pandas as pd
from functools import partial
from typing import Union, Optional, Callable
from canonical_transformer import map_number_to_signed_string
from .consts import MAPPING_INDEX_NAMES
from timeseries_performance_calculator.functionals import pipe

def decorate_table(df: pd.DataFrame, option_round: Union[int, None] = None, option_signed: bool = False) -> pd.DataFrame:
    df = df.copy()
    if option_round is not None:
        df = df.map(lambda value: round(value, option_round))
    if option_signed:
        df = df.map(lambda value: map_number_to_signed_string(value=value, decimal_digits=option_round))
    return df

def rename_as_default_index_names(table: pd.DataFrame) -> pd.DataFrame:
    table = table.rename(index=MAPPING_INDEX_NAMES)
    return table

def decorate(table: pd.DataFrame, option_round: Optional[int] = None, option_signed: bool = False, option_rename_index: bool = True):
    df = table.copy()
    df = decorate_table(df, option_round=option_round, option_signed=option_signed)
    df = rename_as_default_index_names(df) if option_rename_index else df
    return df

def show_table_performance(kernel: Callable[[pd.DataFrame], pd.DataFrame], prices: pd.DataFrame, option_round: Optional[int] = None, option_signed: bool = False, option_rename_index: bool = True) -> pd.DataFrame:
    decorate_with_options = partial(decorate, option_round=option_round, option_signed=option_signed, option_rename_index=option_rename_index)    
    return pipe(
        kernel,
        decorate_with_options
    )(prices)