from functools import cached_property
from universal_timeseries_transformer import PricesMatrix, map_timeserieses_to_list_of_timeserieses
from timeseries_performance_calculator.tables.total import get_table_total_performance, get_dfs_tables_year
from timeseries_performance_calculator.tables.period_returns_table import get_table_period_returns
from timeseries_performance_calculator.tables.yearly_returns_table import get_table_yearly_returns
from timeseries_performance_calculator.tables.monthly_returns_table import get_table_monthly_returns
from timeseries_performance_calculator.basis.return_calculator import calculate_return
from timeseries_performance_calculator.cross_sectional_analysis import get_cross_sectional_performances

class Performance:
    def __init__(self, timeseries, benchmark_column_index=-1):
        self.timeseries = timeseries
        self.benchmark_column_index = benchmark_column_index

    @cached_property
    def list_of_timeserieses(self):
        return map_timeserieses_to_list_of_timeserieses(self.timeseries)

    @cached_property
    def pm(self):
        return PricesMatrix(self.timeseries)
    
    @cached_property
    def prices(self):
        return self.pm.df

    @cached_property
    def returns(self):
        return self.pm.returns
    
    @cached_property
    def cumreturns(self):
        return self.pm.cumreturns
    
    @cached_property
    def total_performance(self):
        if self.timeseries.shape[1] == 1:
            return get_table_total_performance(self.prices, benchmark_column_index=None)
        return get_cross_sectional_performances(self.prices, benchmark_column_index=self.benchmark_column_index)
    
    @cached_property
    def period_returns(self):
        returns = get_table_period_returns(self.prices)
        for i, index in enumerate(returns.index):
            df = self.prices[[index]].dropna()
            returns.iloc[i, -1] = calculate_return(start=df.iloc[0, 0], end=df.iloc[-1, 0])
        return returns
    
    @cached_property
    def yearly_returns(self):
        return get_table_yearly_returns(self.prices)
    
    @cached_property
    def monthly_returns(self):
        return get_table_monthly_returns(self.prices)
    
    @cached_property
    def dfs_tables_year(self):
        return get_dfs_tables_year(self.prices)
    