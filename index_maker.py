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

def download_daily_data(tickers, batch_size=10, timeout=30, retry=5):
    all_data = []
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i+batch_size]
        for attempt in range(retry):
            try:
                data = yf.download(
                    batch,
                    start=start_date,
                    end=end_date,
                    auto_adjust=True,
                    progress=False,
                    threads=True,
                    timeout=timeout
                )['Close']
                all_data.append(data)
                break  # 성공 시 루프 종료
            except Exception as e:
                print(f"Retrying batch {batch}, attempt {attempt+1}/{retry} due to error: {e}")
                time.sleep(2)  # 2초 대기 후 재시도
        else:
            print(f"Failed to download batch {batch} after {retry} attempts.")
    combined_data = pd.concat(all_data, axis=1)
    return combined_data.dropna(axis=1)

stock_daily = download_daily_data(stock_pool, batch_size=10, timeout=30, retry=5)
crypto_daily = download_daily_data(crypto_pool, batch_size=10, timeout=30, retry=5)
commod_daily = download_daily_data(commodity_pool, batch_size=5, timeout=30, retry=5)

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
# 4. Daily Weighted Price Index Calculation
# -----------------------------

def compute_daily_weighted_price_index(prices_df, units):
    index_values = [1000.0]
    dates = [prices_df.index[0]]
    prev_prices = prices_df.iloc[0]

    for current_date, current_prices in prices_df.iloc[1:].iterrows():
        current_mcap = current_prices * pd.Series(units)
        weights = current_mcap / current_mcap.sum()

        daily_return = (current_prices / prev_prices).fillna(1.0)
        daily_weighted_return = (weights * daily_return).sum()

        new_index_value = index_values[-1] * daily_weighted_return
        index_values.append(new_index_value)
        dates.append(current_date)

        prev_prices = current_prices

    return pd.Series(index_values, index=dates)

stock_index = compute_daily_weighted_price_index(stock_daily, stock_shares)
crypto_index = compute_daily_weighted_price_index(crypto_daily, crypto_units)
commod_index = compute_daily_weighted_price_index(commod_daily, commod_units)

# -----------------------------
# 5. Return Indices (초기비중 고정 방식 유지)
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
# 6. Visualization (Plot에 날짜와 최종 값 명시)
# -----------------------------

def plot_indices(price_idx, return_idx, title, color_price, color_return):
    plt.figure(figsize=(12, 6))
    plt.plot(price_idx, linewidth=2, color=color_price, label='Price Index (Daily Weighted)')
    plt.plot(return_idx, linewidth=2, color=color_return, linestyle='--', label='Return Index (No Rebalancing)')

    last_date = price_idx.index[-1].strftime('%Y-%m-%d')
    last_price_val = price_idx.iloc[-1]
    last_return_val = return_idx.iloc[-1]

    plt.annotate(f'{last_date}\nPrice Index: {last_price_val:.2f}',
                 xy=(price_idx.index[-1], last_price_val),
                 xytext=(-150, 20),
                 textcoords='offset points',
                 arrowprops=dict(facecolor=color_price, arrowstyle='->'),
                 fontsize=12, bbox=dict(boxstyle="round,pad=0.3", edgecolor=color_price, alpha=0.2))

    plt.annotate(f'{last_date}\nReturn Index: {last_return_val:.2f}',
                 xy=(return_idx.index[-1], last_return_val),
                 xytext=(-150, -50),
                 textcoords='offset points',
                 arrowprops=dict(facecolor=color_return, arrowstyle='->'),
                 fontsize=12, bbox=dict(boxstyle="round,pad=0.3", edgecolor=color_return, alpha=0.2))

    plt.title(title, fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Index Value', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{title.replace(' ', '_').lower()}.png", dpi=300)
    plt.show()

# Plotting Indices
plot_indices(stock_index, stock_return_index,
             'NASDAQ-100 Index Comparison', 'blue', 'skyblue')

plot_indices(crypto_index, crypto_return_index,
             'Top 20 Cryptocurrencies Index Comparison', 'purple', 'orchid')

plot_indices(commod_index, commod_return_index,
             'Top 10 Commodities Index Comparison', 'green', 'lightgreen')

# -----------------------------
# 7. Display total execution time
# -----------------------------

end_time = time.time()
execution_time = end_time - start_time
print(f"Total Execution Time: {execution_time:.2f} seconds")
