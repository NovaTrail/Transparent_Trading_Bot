# Make indicagor dfs 

try: 
    from preprocess.trading_signals import strategy_map
except ModuleNotFoundError: 
    from trading_signals import strategy_map
import pandas as pd
pd.options.mode.chained_assignment = None 

def col_to_freq(col):
    if "m" in col:
        return col +"in"
    else:
        return col


def convert_to_technicals(price_df,signals_df,strategy_map,col):
    # Produce 12 techincals for each strategy over each time series. 
    # 16 from 4 window sizes and 4 parameters / sensitivity levels. 
    
    # Reverse dataframes as the rolling window is applied top to bottom 
    price_df = price_df.iloc[::-1]
    signals_df = signals_df.iloc[::-1]
    for indicator in strategy_map:
        for level in [1,2,3,4]:
            for window in [12,24,36,55]:
                rolling_window = price_df[col].resample(col_to_freq(col)).ffill().rolling(window)
                flagged_series = rolling_window.apply(lambda row: strategy_map[indicator](row,A=level))
                sampled_back = flagged_series.resample('5min').ffill()
                signals_df.loc[:,f"{indicator}_{col}_{level}_w{window}"] = sampled_back
    return signals_df.copy()[::-1]

def create_signals(price_df,cols = ['5m','15m','1h','4h','12h']):
    """
    Takes input of form: 
    close_time (INDEX),5m,15m,1h,4h,12h
    datetime, float,float,float,float,float
    """
    signals_df = pd.DataFrame(index=price_df.index)

    for col in cols:
        signals_df = convert_to_technicals(price_df,signals_df,strategy_map,col)
    return signals_df  #.dropna().astype(int)



