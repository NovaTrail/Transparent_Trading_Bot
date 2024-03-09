#sSignals 
import numpy as np

def in_bb(price_series,A):
    """
    for an input 1-3 generate a binary output depend on if a price is within the bollinger bands. 
    """
    #price_series = price_series.values()
    threshold = round(2/4 * A,2)
    
    # Calculate the mean and standard deviation of the price series
    mean_value = np.mean(price_series)
    std_value = np.std(price_series)
    # Calculate the z-score
    z_score = (price_series.iloc[-1] - mean_value) / std_value

    # Check if the z-score falls within the buy range (A to B, inclusive)
    if - threshold <= z_score <= threshold:
        return 1
    else:
        return 0

def ma_12_cross(price_series, A):
    """
    Generates a buy or sell signal based on a moving average crossover strategy.

    """
    # Map A to moving average lengths between 12 and 25-70
    period_a = 12 
    period_b = 10 + (A * 15)

    # Calculate the shorter and longer moving averages
    ma_a = np.mean(price_series[-period_a:])
    ma_b = np.mean(price_series[-period_b:])

    # Check for the moving average crossover
    if ma_a > ma_b:
        return 1
    else:
        return 0

def rsi_signal(price_series, A):
    # Calculate the price changes
    price_changes = np.diff(price_series)

    # Calculate the positive and negative price changes
    avg_gain = np.mean(np.where(price_changes > 0, price_changes, 0))
    avg_loss = np.mean(np.where(price_changes < 0, -price_changes, 0))

    # Calculate the RSI value
    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # Map A to appropriate RSI thresholds
    lower_threshold = 30 - (5*A)
    upper_threshold = 70 + (5*A)

    if lower_threshold <= rsi <= upper_threshold:
        return 1
    else:
        return 0
    
def drawdown(price_series, A):
    #calculate the drawdown from the local peak 
    rolling_max = np.maximum.accumulate(price_series).iloc[-1]
    drawdown_perc = (100*(price_series.iloc[-1]-rolling_max) / rolling_max)

    # and compare to the threshold
    lower_threshold = -A 
    if lower_threshold <= drawdown_perc:
        return 1
    else:
        return 0 

strategy_map = {
    'bb':in_bb,
    'ma12':ma_12_cross,
    'rsi':rsi_signal,
    'dd':drawdown,
    }


