
## Thesis
## To automate trading of fundamentally viable momentum stocks experiencing volatility dislocations
## entering only when trend, volume, and bounce signals align
## while managing each position with ATR-based sizing and dynamic stops for short-term 
## run through vs code, conda with jupyter notebook, API from databento or alpaca

## This approach is meant to test and emulate a singular niche trading strategy for fundamentally viable small-cap and mid-cap stocks experiencing sudden, retail-driven liquidity shocks (volatility dislocations) 
## while mitigating risk and delivering outsized moves in a systematic, rule-driven manner
## When the below mechanical trading approach is combined with a high-fidelity data pipeline, a sentiment analysis model, and extreme backtests (easier said than done)  it may or may not prove to have a positive expected value
## thus serving as a viable systematic trading signal
##As a resource to aid the development of the above trading strategy, I will continue to refine the model's predictive power,
## validate the risk controls, and prepare architeture for deployment



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
# request 6 months of data at 1 hr interval and use different data source than y finance
data = yf.download(ticker, period='6mo', interval='1h') 

if data.empty:
    print(f"Data download failed for {ticker}. The ticker may not exist or yfinance limits were hit.")
else:
    # drop rows with any NaN values that can appear at start/end of day
    data.dropna(inplace=True)
    print(f"Downloaded {len(data)} rows of 1-Hour data for {ticker}.")
    data.head()


## feature engineering for bounce and continuation

# A. volatility and trend indicators
data['ATR_14'] = ta.volatility.AverageTrueRange(data['High'], data['Low'], data['Close'], window=14).average_true_range()
data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
data['SMA_50'] = ta.trend.sma_indicator(data['Close'], window=50)

# B. momentum/oversold indicators
data['RSI_14'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
stoch = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'], window=14, smooth_window=3)
data['Stoch_K'] = stoch.stoch()
data['Stoch_D'] = stoch.stoch_signal()

# C. volume/flow dislocation
data['FI_2'] = ta.volume.ForceIndexIndicator(data['Close'], data['Volume'], window=2).force_index()
data['Vol_Avg_20'] = data['Volume'].rolling(window=20).mean()
data['Vol_Ratio'] = data['Volume'] / data['Vol_Avg_20'] # measures volume surge

## quantified features for bounce strategy 

# 1. deviance from short-term trend 
data['EMA_Dev'] = (data['Close'] - data['EMA_20']) / data['Close']

# 2. oversold depth 
data['RSI_Oversold_Depth'] = np.where(data['RSI_14'] < 50, 50 - data['RSI_14'], 0)

# 3. volatility context 
data['ATR_Norm'] = data['ATR_14'] / data['Close']

# 4. mechanical rules as features 
data['Trend_Reest'] = np.where(data['Close'] > data['EMA_20'], 1, 0)
data['RSI_Curl'] = data['RSI_14'].diff()

data.dropna(inplace=True)
print(f"Data shape after optimized feature engineering: {data.shape}")


## optimmized target variable 

N_BARS = 35        # look 35 1-Hour bars (5 trading days) into the future
THRESHOLD = 0.10  # target return of 5-10%

data['Future_Return'] = data['Close'].pct_change(N_BARS).shift(-N_BARS)

data['Target'] = 0

data.loc[data['Future_Return'] > THRESHOLD, 'Target'] = 1

# exclude short-selling 
data.loc[data['Future_Return'] < -THRESHOLD, 'Target'] = np.nan 

data.dropna(subset=['Target'], inplace=True) 
data.dropna(inplace=True) 

print("Target variable distribution (Focus on Buy/Hold):")
print(data['Target'].value_counts())


## timeseriessplit + tuning

# features and target
features = [
    'ATR_14', 'EMA_20', 'SMA_50', 'RSI_14', 'Stoch_K', 'Stoch_D', 
    'FI_2', 'Vol_Ratio', 'Trend_Reest', 'RSI_Curl', 'Close', 'Volume',
    'EMA_Dev', 'RSI_Oversold_Depth', 'ATR_Norm'
]
X = data[features]
y = data['Target'].astype(int)

# time-series CV
tscv = TimeSeriesSplit(n_splits=5)

# scaling (fit only on training folds inside GridSearch)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# precision on positive class
precision_scorer = make_scorer(precision_score, pos_label=1)

# hyperparameter grid
param_grid = {
    'n_estimators': [150, 250],
    'max_depth': [8, 12],
    'min_samples_split': [5, 10],
    'class_weight': ['balanced', 'balanced_subsample']
}

# grid search with time-series CV
rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    scoring=precision_scorer,
    cv=tscv,
    n_jobs=-1
)
grid_search.fit(X_scaled, y)
best_model = grid_search.best_estimator_

print("Best Model Parameters:", grid_search.best_params_)

# final train/test split from last fold
split = list(tscv.split(X_scaled))[-1][0].stop
X_train_final, X_test_final = X_scaled[:split], X_scaled[split:]
y_train_final, y_test_final = y[:split], y[split:]


## optimized model evaluation 

# make predictions on test set 
y_pred = best_model.predict(X_test_final)

# classifications report of test data 
print("--- Classification Report (Test Data) ---")
print(classification_report(y_test_final, y_pred, zero_division=0))

# get feature importance 
importance = pd.Series(best_model.feature_importances_, index=features).sort_values(ascending=False)
print("\n--- Feature Importance (from Best Model) ---")
print(importance)


# key metric check for analysis 

final_precision = precision_score(y_test_final, y_pred, pos_label=1, zero_division=0)
print(f"\nOPTIMIZED KEY METRIC: PRECISION for BUY (1): {final_precision:.4f}")


## All code above functions as a statistical report. It does not account for slippage, commissions, or outlined complex ATR-based risk management rules
## The ML model might have high precision, but if the signal fires when the stock is already extended (high volatility), stop loss might be immediately hit, causing a net loss
## This calls for integration of the model into a robust backtesting framework (ie. backtesting.py or backtrader) where you can hard-code the risk management logic
## This code only tests one screener (ie. ticker $QS) and cannot automate the Gross Profit Margin or Institutional Ownership filters using just yfinance
## Before automating, you need a separate script or tool to scan the entire market against your fundamental/liquidity rules and output the 5-10 tickers
## which then become the input for current model
## Above code is a simple mechanical trading solution that paves the way for Backtesting phase to integrate risk management rules and verify validity of above statistical model
