# Import necessary libraries
import pandas as pd
from datetime import datetime, timedelta

from create_signals_df import create_signals
from data_source import get_historical_data

# Define parameters for fetching data
symbol = 'BTCUSDT'  # Trading pair
candles = ["5m","15m","1h","2h","6h"]
year = 2023
half = 1

if half ==1: 
    start_str = f'{year}-01-01'  # Start date
    end_str = f'{year}-07-01'  # End date
elif half == 2:
    start_str = f'{str(year)}-07-01'  # Start date
    end_str = f'{str(year+1)}-01-01'  # End date


# Add time to each side of the data
# extra data before start for moving averages  
start_datetime = datetime.strptime(start_str, '%Y-%m-%d')
_new_start_str = (start_datetime - timedelta(days=20)).strftime('%Y-%m-%dT%H:%M')

# extra data after end for outcome labels
end_datetime = datetime.strptime(end_str, '%Y-%m-%d')
_new_end_str = (end_datetime + timedelta(hours=10)).strftime('%Y-%m-%dT%H:%M')

def get_klines_to_df(symbol, interval,_new_start_str,_new_end_str ):
    """
    Fetch historical data and return as a DataFrame.
    
    Parameters:
        symbol (str): Trading symbol (e.g., 'BTCUSDT')
        interval (str): Kline interval (e.g., '5m', '15m', '1h')
        start_str (str): Start date in string format
        end_str (str): End date in string format
        
    Returns:
        DataFrame: Processed DataFrame with selected columns
    """

    # Fetch historical klines from Binance
    candles = get_historical_data(symbol, interval, _new_start_str,_new_end_str)
    # Create DataFrame and name columns
    df = pd.DataFrame(candles, columns=['open', 'high', 'low', 'close','close_time'])

    # Convert 'close_time' to datetime and set 'open_time' as index
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    df.set_index('close_time', inplace=True)
    # Select and convert relevant columns to float
    df = df[['open', 'high', 'low', 'close']].astype(float)
    #resample to 5 minutes
    df= df.resample(f'{candles[0]}in').ffill()
    return df

# Create a initial dataset with the correct index
price_df = pd.DataFrame(index=get_klines_to_df(symbol, candles[0],_new_start_str,_new_end_str).index)

# Loop through desired intervals for additional data fetching and processing
for series in candles:
    # Fetch and process data for each interval
    df_xm = get_klines_to_df(symbol, series,_new_start_str,_new_end_str)

    # average price 
    price_df[f'{series}'] = round(((df_xm['high'] + df_xm['low'] + df_xm['close']) / 3),3)


# get signals df
signals_df = create_signals(price_df,cols=candles)


## Add labels to the datasets
# price_df        
price_df['L10'] = round(((price_df['5m'].shift(-2) / price_df['5m'])-1)*100,2)
price_df['L20'] = round(((price_df['5m'].shift(-4) / price_df['5m'])-1)*100,2)
price_df['L30'] = round(((price_df['5m'].shift(-6) / price_df['5m'])-1)*100,2)
price_df['L60'] = round(((price_df['5m'].shift(-12) / price_df['5m'])-1)*100,2)
#signals_df 
signals_df[['L10', 'L20','L30','L60']] = price_df[['L10', 'L20','L30','L60']]

# Crop to the designated dates, 
price_df = price_df.loc[start_str:end_str]
signals_df = signals_df.loc[start_str:end_str]

#Then drop rows with any NaN values 
price_df = price_df.dropna()
signals_df = signals_df.dropna() 

price_df.to_csv(f'preprocess\historical_data\{symbol}\Price_{str(year)}H{str(half)}.csv')
signals_df.to_csv(f"preprocess\historical_data\{symbol}\signals_{str(year)}H{str(half)}.csv")