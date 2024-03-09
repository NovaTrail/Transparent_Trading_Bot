#import_data.py 
import pandas as pd

## import data 
df1 = pd.read_csv("preprocess/historical_data/BTCUSDT/signals_2023H1.csv")
df1.set_index('close_time', inplace=True)
df2 = pd.read_csv("preprocess/historical_data/BTCUSDT/signals_2023H2.csv")
df2.set_index('close_time', inplace=True)

df_lst = [df1,df2]

df = pd.concat(df_lst)
df.index = pd.to_datetime(df.index)
df = df.dropna(axis=0)

X = df.resample('20min').first()

X.reset_index(inplace=True)
X = X.drop(columns=['close_time'])

# 20 min  delta steps for backtest
yd =  X['L20']

# regression 
yc = X['L20'].apply(lambda x: 1 if x > 0.4 else 0 )

X = X.drop(['L10', 'L20','L30','L60'],axis=1)