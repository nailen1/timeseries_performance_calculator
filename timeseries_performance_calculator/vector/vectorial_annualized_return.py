# vectorial_annualized_return.py

from .annualized_return_calculator import calculate_annualized_return_cagr, calculate_annualized_return_days
import pandas as pd

def calculate_cumreturn_of_timeseries(timeseries: pd.Series)->float:
    price_i = timeseries.iloc[0]
    price_f = timeseries.iloc[-1]
    return (price_f / price_i - 1) * 100

def get_trading_days_of_timeseries(timeseries: pd.Series)->int:
    return len(timeseries)

def calculate_annualized_return_of_timeseries(timeseries: pd.Series, calculator)->float:
    cumreturn = calculate_cumreturn_of_timeseries(timeseries)
    trading_days = get_trading_days_of_timeseries(timeseries)
    return calculator(cumreturn=cumreturn, trading_days=trading_days)

def calculate_cagr_of_timeseries(timeseries: pd.Series)->float:
    return calculate_annualized_return_of_timeseries(timeseries, calculate_annualized_return_cagr)

def calculate_annualized_days_return_of_timeseries(timeseries: pd.Series)->float:
    return calculate_annualized_return_of_timeseries(timeseries, calculate_annualized_return_days)