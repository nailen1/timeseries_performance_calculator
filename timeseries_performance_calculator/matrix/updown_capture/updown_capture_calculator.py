import pandas as pd
from financial_dataset_preprocessor.preprocess_consts import RETURNS_PREFIX

def get_data_updown_capture(df_returns_with_benchmark, benchmark):
    if df_returns_with_benchmark.shape[1] != 2:
        raise ValueError("DataFrame must have exactly 2 columns")
    df = df_returns_with_benchmark.copy()
    cols = df.columns
    col_portfolio = [col for col in cols if benchmark not in col][0]
    col_benchmark = [col for col in cols if benchmark in col][0]
    name_portfolio = col_portfolio.replace(RETURNS_PREFIX, '')
    name_benchmark = col_benchmark.replace(RETURNS_PREFIX, '')
    df_up = df[df[col_benchmark].apply(lambda x: x >= 0)]
    df_up_mean = df_up.mean()
    mean_up_portfolio = df_up_mean[col_portfolio]
    mean_up_benchmark = df_up_mean[col_benchmark]
    upside_capture = mean_up_portfolio / mean_up_benchmark
    df_down = df[df[col_benchmark].apply(lambda x: x < 0)]
    df_down_mean = df_down.mean()
    mean_down_portfolio = df_down_mean[col_portfolio]
    mean_down_benchmark = df_down_mean[col_benchmark]
    downside_capture = mean_down_portfolio / mean_down_benchmark
    capture_ratio = upside_capture / downside_capture
    dct = {'portfolio': name_portfolio, 'code_benchmark': name_benchmark, 'capture_ratio': capture_ratio, 'upside_capture': upside_capture, 'downside_capture': downside_capture, 'mean_up_portfolio': mean_up_portfolio, 'mean_up_benchmark': mean_up_benchmark, 'mean_down_portfolio': mean_down_portfolio, 'mean_down_benchmark': mean_down_benchmark}
    return dct

def get_updown_capture_of_multi_timeseries(df_returns_with_benchmark, benchmark):
    lst = []
    cols = df_returns_with_benchmark.columns
    col_benchmark = [col for col in cols if benchmark in col][0]
    for col in df_returns_with_benchmark.columns:
        if col_benchmark not in col:
            df = df_returns_with_benchmark[[col, col_benchmark]]
            data_updown_capture = get_data_updown_capture(df, benchmark)
            portfolio = data_updown_capture['portfolio']
            capture_ratio = data_updown_capture['capture_ratio']
            lst.append({'portfolio': portfolio, 'capture_ratio': capture_ratio})
        else:
            lst.append({'portfolio': benchmark, 'capture_ratio': '-'})
    df = pd.DataFrame(lst).set_index('portfolio').T
    df.columns.name = None
    return df
