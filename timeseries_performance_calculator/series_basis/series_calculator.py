import pandas as pd
from timeseries_performance_calculator.basis import calculate_return

def calculate_series_cumreturns_between_dates(timeseries: pd.Series, date_i: str, date_f: str = None) -> pd.Series:
    date_f = date_f if date_f is not None else timeseries.index[-1]
    start_value = timeseries.loc[date_i]
    end_value = timeseries.loc[date_f]
    return calculate_return(start_value, end_value)