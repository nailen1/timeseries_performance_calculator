import numpy as np

def calculate_beta_numpy(target_returns, benchmark_returns):
    if len(target_returns) != len(benchmark_returns):
        raise ValueError("Both lists must have the same length")
        
    target_arr = np.array(target_returns)
    benchmark_arr = np.array(benchmark_returns)
    
    return np.cov(target_arr, benchmark_arr)[0,1] / np.var(benchmark_arr)

def calculate_beta_optimized(target_returns, benchmark_returns):
    if len(target_returns) != len(benchmark_returns):
        raise ValueError("Both lists must have the same length")
        
    n = len(target_returns)
    sum_target = sum(target_returns)
    sum_benchmark = sum(benchmark_returns)
    
    # Single pass for all required sums
    sum_target_benchmark = 0
    sum_benchmark_squared = 0
    
    for i in range(n):
        sum_target_benchmark += target_returns[i] * benchmark_returns[i]
        sum_benchmark_squared += benchmark_returns[i] * benchmark_returns[i]
    
    mean_target = sum_target / n
    mean_benchmark = sum_benchmark / n
    
    covariance = (sum_target_benchmark - n * mean_target * mean_benchmark) / (n - 1)
    variance = (sum_benchmark_squared - n * mean_benchmark * mean_benchmark) / (n - 1)
    
    return covariance / variance