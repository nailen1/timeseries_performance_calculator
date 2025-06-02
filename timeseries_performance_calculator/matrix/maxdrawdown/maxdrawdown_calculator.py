import pandas as pd
from financial_dataset_preprocessor.preprocess_consts import CUMRETURNS_PREFIX

def get_df_drawdown_of_timeseries(df_cumreturns):
    if df_cumreturns.shape[1] != 1:
        raise ValueError("DataFrame must have exactly one column")
    df = df_cumreturns.copy()
    df['trough'] = df.iloc[:, 0]/100 + 1
    df['historical_peak'] = df['trough'].cummax()
    mapping_trough_to_date = df.reset_index().drop_duplicates('trough').set_index('trough')['date'].to_dict()
    df['date_peak'] = df['historical_peak'].map(mapping_trough_to_date)
    df['drawdown'] = (df['trough'] / df['historical_peak'] - 1)*100
    return df

def get_data_maxdrawdown(df_drawdown):
    df = df_drawdown.reset_index()
    portfolio = df.columns[1].replace(CUMRETURNS_PREFIX, '')
    index = df['drawdown'].idxmin()
    row = df.loc[index].to_dict()
    dates_in_df = list(df['date'].dropna())
    start_date = dates_in_df[0]
    end_date = dates_in_df[-1]
    period_mdd = len(df[(df['date']>=row['date_peak'])&(df['date']<=row['date'])])
    dct = {'portfolio': portfolio, 'start_date': start_date, 'end_date': end_date, 'mdd': row['drawdown'], 'peak': row['historical_peak'], 'trough': row['trough'], 'date_peak': row['date_peak'], 'date_trough': row['date'], 'period_mdd':period_mdd}
    return dct

def get_maxdrawdown(data_maxdrawdown):
    return data_maxdrawdown['mdd']

def get_maxdrawdown_of_multi_timeseries(df_cumreturns):
    columns = df_cumreturns.columns
    lst = []
    for col in columns:
        df_cumreturn = df_cumreturns[[col]]
        df_drawdown = get_df_drawdown_of_timeseries(df_cumreturns=df_cumreturn)
        data_drawdown = get_data_maxdrawdown(df_drawdown)
        portfolio = data_drawdown['portfolio']
        maxdrawdown = get_maxdrawdown(data_drawdown)
        dct = {'portfolio': portfolio, 'maxdrawdown': maxdrawdown}
        lst.append(dct)
    df = pd.DataFrame(lst).set_index('portfolio').T
    df.columns.name = None
    return df
