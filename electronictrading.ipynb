# developing momentum trading algorithms for testing
# Thesis: 
# target fundamentally viable, low-liquidity momentum stocks experiencing volatility dislocations
# entering only when trend, volume, and bounce signals align
# while managing each position with ATR-based sizing and dynamic stops for short-term 


## data acquisition 

import yfinance as yf
import pandas as pd
import ta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import make_scorer, precision_score


# enter stock ticker 
ticker = 'QS' 
# request 6 months of data at 1 hr interval and use different api (databento/alpaca)
data = yf.download(ticker, period='6mo', interval='1h') 

if data.empty:
    print(f"Data download failed for {ticker}. The ticker may not exist or yfinance limits were hit.")
else:
    # drop rows with any NaN values that can appear at start/end of day
    data.dropna(inplace=True)
    print(f"Downloaded {len(data)} rows of 1-Hour data for {ticker}.")
    data.head()


## feature engineering for bounce and continuation

# A. Volatility and Trend Indicators
data['ATR_14'] = ta.volatility.AverageTrueRange(data['High'], data['Low'], data['Close'], window=14).average_true_range()
data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
data['SMA_50'] = ta.trend.sma_indicator(data['Close'], window=50)

# B. Momentum/Oversold Indicators
data['RSI_14'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
stoch = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'], window=14, smooth_window=3)
data['Stoch_K'] = stoch.stoch()
data['Stoch_D'] = stoch.stoch_signal()

# C. Volume/Flow Dislocation
data['FI_2'] = ta.volume.ForceIndexIndicator(data['Close'], data['Volume'], window=2).force_index()
data['Vol_Avg_20'] = data['Volume'].rolling(window=20).mean()
data['Vol_Ratio'] = data['Volume'] / data['Vol_Avg_20'] # Measures volume surge

## quantified features for bounce strategy 

# 1. Deviance from Short-Term Trend (How stretched the price is)
data['EMA_Dev'] = (data['Close'] - data['EMA_20']) / data['Close']

# 2. Oversold Depth (Quantifies severity of the bounce potential)
# Measures how far RSI is below 50, capped at 0 (only active when RSI < 50)
data['RSI_Oversold_Depth'] = np.where(data['RSI_14'] < 50, 50 - data['RSI_14'], 0)

# 3. Volatility Context (Normalizing ATR by Price)
data['ATR_Norm'] = data['ATR_14'] / data['Close']

# 4. Mechanical Rules as Features
data['Trend_Reest'] = np.where(data['Close'] > data['EMA_20'], 1, 0)
data['RSI_Curl'] = data['RSI_14'].diff()

data.dropna(inplace=True)
print(f"Data shape after optimized feature engineering: {data.shape}")
