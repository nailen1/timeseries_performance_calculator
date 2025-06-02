import pandas as pd
from itertools import starmap
from universal_timeseries_transformer import TimeseriesMatrix
from string_date_controller import get_all_data_historical_dates

def calculate_cumreturns_table_between_dates(timeseries: pd.DataFrame, date_i: str, date_f: str = None, label_cumreturn:str = 'cumreturn') -> pd.DataFrame:
    date_f = date_f if date_f is not None else timeseries.index[-1]
    rows = timeseries.copy().loc[[date_i, date_f], :]
    rows.loc[label_cumreturn, :] = (rows.iloc[-1] / rows.iloc[0] - 1) * 100
    return rows

def get_cumreturns_row_between_dates(timeseries: pd.DataFrame, date_i: str, date_f: str = None, label_cumreturn:str = 'cumreturn') -> pd.DataFrame:
    table = calculate_cumreturns_table_between_dates(timeseries, date_i, date_f, label_cumreturn)
    row = table.iloc[[-1]]
    row.index.name = 'period'
    return row

def get_period_cumreturn_table(timeseries: pd.DataFrame) -> pd.DataFrame:
    tm = TimeseriesMatrix(timeseries)
    dates = tm.dates
    dct_dates = get_all_data_historical_dates(dates)

    return pd.concat(
        starmap(lambda label, date: get_cumreturns_row_between_dates(tm.df, date_i=date, label_cumreturn=label), 
                dct_dates.items()), 
    axis=0
)