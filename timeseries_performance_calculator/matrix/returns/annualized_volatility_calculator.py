import pandas as pd
import numpy as np
from string_date_controller import get_initial_date_of_timeseries, get_final_date_of_timeseries
from financial_dataset_preprocessor.preprocess_consts import RETURNS_PREFIX

ANNUAL_TRADING_DAYS = 252

def get_annualized_volatility_of_timeseries(df_returns, annual_trading_days=ANNUAL_TRADING_DAYS):
    if df_returns.shape[1] != 1:
        raise ValueError("DataFrame must have exactly one column")
    std = df_returns.std().iloc[0]
    annualized_volatility = std * np.sqrt(annual_trading_days)
    return annualized_volatility

def get_annualized_volatility_of_multi_timeseries(df_returns, annual_trading_days=ANNUAL_TRADING_DAYS, option_period_manifest=False):
    initial_date_in_df = get_initial_date_of_timeseries(df_returns)
    final_date_in_df = get_final_date_of_timeseries(df_returns)
    srs_std = df_returns.std()
    df_std = pd.DataFrame(srs_std)
    df = df_std * np.sqrt(annual_trading_days)
    df = (df.copy()
          .pipe(lambda x: x.rename(columns={x.columns[0]: f'annualized_volatility'}))
          .pipe(lambda x: x.rename_axis(f'({initial_date_in_df}, {final_date_in_df})') if option_period_manifest else x)
          .pipe(lambda x: x.T)
          .pipe(lambda x: x.rename(columns={col: f"{col.replace(f'{RETURNS_PREFIX}','')}" for col in x.columns}))
          )
    return df
