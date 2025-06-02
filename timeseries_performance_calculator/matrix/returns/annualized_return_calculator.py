from universal_timeseries_transformer import slice_timeseries_by_dates
from .period_return_calculator import get_period_return_of_timeseries, get_period_return_of_multi_timeseries

def calculate_annualized_return_cagr(cumreturn, trading_days):
    annualized_return_cagr = ((1+cumreturn/100)**(365/trading_days)-1)*100
    return annualized_return_cagr    

def get_annualized_return_cagr_of_timeseries(df, start_date, end_date):
    df = slice_timeseries_by_dates(df, start_date, end_date)
    trading_days = len(df)
    cumreturn = get_period_return_of_timeseries(df, start_date=start_date, end_date=end_date)
    annualized_return_cagr = calculate_annualized_return_cagr(cumreturn=cumreturn, trading_days=trading_days)
    return annualized_return_cagr

def get_annualized_return_cagr_of_multi_timeseries(df, start_date, end_date, option_period_manifest=False):
    df = slice_timeseries_by_dates(df, start_date, end_date)
    trading_days = len(df)
    df_cumreturn = get_period_return_of_multi_timeseries(df=df, start_date=start_date, end_date=end_date, option_period_manifest=option_period_manifest)
    df_annualized_return_cagr = calculate_annualized_return_cagr(cumreturn=df_cumreturn, trading_days=trading_days)
    df_annualized_return_cagr.index = ['annualized_return_cagr']
    return df_annualized_return_cagr

def calculate_annualized_return_days(cumreturn, trading_days):
    number_of_days = trading_days-1
    annualized_return_days = round(cumreturn/number_of_days*365, 2)
    return annualized_return_days

def get_annualized_return_days_of_timeseries(df, start_date=None, end_date=None):
    if start_date is None and end_date is None:
        df = slice_timeseries_by_dates(df, start_date, end_date)
    trading_days = len(df)
    cumreturn = get_period_return_of_timeseries(df)
    annualized_return_days = calculate_annualized_return_days(cumreturn=cumreturn, trading_days=trading_days)
    return annualized_return_days

def get_annualized_return_days_of_multi_timeseries(df, start_date=None, end_date=None, option_period_manifest=False):
    if start_date is None and end_date is None:
        df = slice_timeseries_by_dates(df, start_date, end_date)
    trading_days = len(df)
    df_cumreturn = get_period_return_of_multi_timeseries(df=df, start_date=start_date, end_date=end_date, option_period_manifest=option_period_manifest)
    df_annualized_return_days = calculate_annualized_return_days(cumreturn=df_cumreturn, trading_days=trading_days)
    df_annualized_return_days.index = ['annualized_return_days']
    return df_annualized_return_days