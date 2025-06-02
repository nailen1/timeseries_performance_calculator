from universal_timeseries_transformer import extend_timeseries_by_all_dates
from financial_dataset_preprocessor import load_index
from string_date_controller import get_initial_date_of_timeseries, get_final_date_of_timeseries
import pandas as pd
from universal_timeseries_transformer import slice_timeseries_by_dates
# from report_generator.yfinance_loader import load_ewy


def get_two_points_timeseries(timeseries, start_date=None, end_date=None):
    df = timeseries.copy()
    df = slice_timeseries_by_dates(df, start_date, end_date)
    initial_date_in_df = get_initial_date_of_timeseries(df)
    final_date_in_df = get_final_date_of_timeseries(df)
    df_i_and_f = df.loc[[initial_date_in_df, final_date_in_df]]
    return df_i_and_f

def get_period_return_of_timeseries(df, start_date=None, end_date=None):
    if df.shape[1] != 1:
        raise ValueError("DataFrame must have exactly one column")
    initial_date_in_df = get_initial_date_of_timeseries(df)
    start_date = initial_date_in_df if initial_date_in_df > start_date else start_date
    df = slice_timeseries_by_dates(df, start_date, end_date)
    print(f'calculating period return: {start_date} ~ {end_date}')
    cumreturn = (df.iloc[-1] / df.iloc[0] - 1) * 100
    return cumreturn.iloc[0]

def get_period_return_of_multi_timeseries(df, start_date=None, end_date=None, option_period_manifest=False):
    df_i_and_f = get_two_points_timeseries(df, start_date, end_date)
    initial_date_in_df = get_initial_date_of_timeseries(df_i_and_f)
    final_date_in_df = get_final_date_of_timeseries(df_i_and_f)
    cumreturn = (df_i_and_f.iloc[-1] / df_i_and_f.iloc[0] - 1) * 100
    df = pd.DataFrame(cumreturn)
    df = (df.copy()
          .pipe(lambda x: x.rename(columns={x.columns[0]: f'cumreturn'}))
          .pipe(lambda x: x.rename_axis(f'({initial_date_in_df}, {final_date_in_df})') if option_period_manifest else x)
          .pipe(lambda x: x.T)
          )
    return df

def get_preriod_return_of_multi_timeseries_with_price_info(df, start_date=None, end_date=None):
    df_i_and_f = get_two_points_timeseries(df, start_date=start_date, end_date=end_date).T
    df_i_and_f['cumreturn'] = (df_i_and_f.iloc[:, -1] / df_i_and_f.iloc[:, 0] - 1) * 100
    return df_i_and_f.T

from shining_pebbles import open_df_in_file_folder_by_regex

def load_prices(date_ref):
    regex = f'dataset-prices-.*to{date_ref.replace("-","")}'
    prices = open_df_in_file_folder_by_regex(file_folder='dataset', regex=regex)
    return prices

def load_net_performance(date_ref):
    regex = f'dataset-net_performance-.*to{date_ref.replace("-","")}'
    net_performance = open_df_in_file_folder_by_regex(file_folder='dataset', regex=regex)
    return net_performance

def get_two_points_return(df, start_date, end_date):
    COLUMNE_NAME_FOR_PRICE = 'PX_LAST'
    df.columns = [COLUMNE_NAME_FOR_PRICE]
    two_points = df.loc[[start_date, end_date], :]
    start_price = two_points.loc[start_date, COLUMNE_NAME_FOR_PRICE]
    end_price = two_points.loc[end_date, COLUMNE_NAME_FOR_PRICE]
    two_points.loc['return', COLUMNE_NAME_FOR_PRICE] = (end_price / start_price - 1) * 100
    return two_points

# def get_ewy_return(start_date, end_date):
#     ewy = load_ewy()
#     return get_two_points_return(df=ewy, start_date=start_date, end_date=end_date)
    
# def get_mxkr_return(start_date, end_date):
#     mxkr = extend_timeseries_by_all_dates(load_index(ticker_bbg_index='MXKR Index'))    
#     return get_two_points_return(df=mxkr, start_date=start_date, end_date=end_date)

# def get_m1kr_return(start_date, end_date):
#     m1kr = extend_timeseries_by_all_dates(load_index(ticker_bbg_index='M1KR Index'))    
#     return get_two_points_return(df=m1kr, start_date=start_date, end_date=end_date)

# # def get_lkef_return(start_date, end_date):
# #     lkef = load_prices(end_date)[['LKEF']]
# #     return get_two_points_return(df=lkef, start_date=start_date, end_date=end_date)