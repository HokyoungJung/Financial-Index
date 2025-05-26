import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
import time

start_time = time.time()  # Start measuring execution time

# Date Range
start_date = "2019-01-01"
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# -----------------------------
# 1. Automatically update asset pools
# -----------------------------

# NASDAQ-100 stocks from Wikipedia
def get_nasdaq100():
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    tickers = pd.read_html(url)[4]['Ticker'].tolist()
    return [t.replace('.', '-') for t in tickers]

# Top 20 Cryptocurrencies by market cap from CoinGecko
def get_crypto_pool(top_n=20):
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=top_n)
    return [coin['symbol'].upper()+'-USD' for coin in coins]

# Fixed Commodity Pool (Yahoo Finance tickers)
commodity_pool = ["GC=F","SI=F","CL=F","HG=F","NG=F","ZC=F","ZS=F","ZW=F","KC=F","CT=F"]

# Retrieve current asset pools
stock_pool = get_nasdaq100()
crypto_pool = get_crypto_pool(20)

# -----------------------------
# 2. Download daily data
# -----------------------------

def download_daily_data(tickers):
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, progress=False)['Close']
    return data.dropna(axis=1)

stock_daily = download_daily_data(stock_pool)
crypto_daily = download_daily_data(crypto_pool)
commod_daily = download_daily_data(commodity_pool)

# -----------------------------
# 3. Initial Market Caps and Units
# -----------------------------

# Get shares outstanding for stocks
def get_shares(tickers):
    shares = {}
    for ticker in tickers:
        try:
            sh = yf.Ticker(ticker).info.get('sharesOutstanding', np.nan)
            if sh: shares[ticker] = sh
        except:
            continue
    return pd.Series(shares).dropna()

stock_shares = get_shares(stock_daily.columns)
stock_daily = stock_daily[stock_shares.index]

# Get initial crypto market caps from CoinGecko
def get_crypto_initial_caps(crypto_symbols):
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=20)
    caps = {coin['symbol'].upper()+'-USD': coin['market_cap'] for coin in coins}
    return {sym: caps[sym] for sym in crypto_symbols if sym in caps}

crypto_caps = get_crypto_initial_caps(crypto_daily.columns)
crypto_units = {c: crypto_caps[c]/crypto_daily.iloc[0][c] for c in crypto_daily.columns}

# Equal initial investment ($100 each) in commodities
commod_units = {c: 100/commod_daily.iloc[0][c] for c in commod_daily.columns}

# -----------------------------
# 4. Daily Price Index with Monthly Rebalancing
# -----------------------------

def compute_index_daily_monthly_rebal(prices_df, units):
    idx_values = [1000.0]
    dates = [prices_df.index[0]]

    current_weights = (prices_df.iloc[0] * pd.Series(units))
    current_weights /= current_weights.sum()

    prev_prices = prices_df.iloc[0]

    for current_date, current_prices in prices_df.iloc[1:].iterrows():
        daily_return = (current_prices / prev_prices).fillna(1.0)
        daily_index_return = (current_weights * daily_return).sum()

        new_index = idx_values[-1] * daily_index_return
        idx_values.append(new_index)
        dates.append(current_date)

        if current_date == (current_date + pd.tseries.offsets.MonthEnd(0)):
            current_weights = (current_prices * pd.Series(units))
            current_weights /= current_weights.sum()

        prev_prices = current_prices

    return pd.Series(idx_values, index=dates)

stock_index = compute_index_daily_monthly_rebal(stock_daily, stock_shares)
crypto_index = compute_index_daily_monthly_rebal(crypto_daily, crypto_units)
commod_index = compute_index_daily_monthly_rebal(commod_daily, commod_units)

# -----------------------------
# 5. Calculate Return Indices (No Rebalancing, cumulative returns)
# -----------------------------

def compute_return_index(prices_df, units):
    returns = prices_df.pct_change().fillna(0)
    weights = (prices_df.iloc[0] * pd.Series(units))
    weights /= weights.sum()
    weighted_returns = returns.dot(weights)
    return_index = (1 + weighted_returns).cumprod() * 1000
    return return_index

stock_return_index = compute_return_index(stock_daily, stock_shares)
crypto_return_index = compute_return_index(crypto_daily, crypto_units)
commod_return_index = compute_return_index(commod_daily, commod_units)

# -----------------------------
# 6. Visualize Both Indices
# -----------------------------

def plot_indices(price_idx, return_idx, title, color_price, color_return):
    plt.figure(figsize=(12,6))
    plt.plot(price_idx, linewidth=2, color=color_price, label='Price Index (Monthly Rebalancing)')
    plt.plot(return_idx, linewidth=2, color=color_return, linestyle='--', label='Return Index (No Rebalancing)')
    plt.title(title, fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Index Value', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

plot_indices(stock_index, stock_return_index, 'NASDAQ-100 Index Comparison', 'blue', 'skyblue')
plot_indices(crypto_index, crypto_return_index, 'Top 20 Cryptocurrencies Index Comparison', 'purple', 'orchid')
plot_indices(commod_index, commod_return_index, 'Top 10 Commodities Index Comparison', 'green', 'lightgreen')

# -----------------------------
# 7. Display total execution time
# -----------------------------

end_time = time.time()
execution_time = end_time - start_time
print(f"Total Execution Time: {execution_time:.2f} seconds")
