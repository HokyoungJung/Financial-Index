# 📈 Market-Cap-Weighted Indices (Stocks, Cryptocurrencies, Commodities)

This repository provides an automated calculation and intuitive visualization of market-cap-weighted financial indices for three major asset classes:

* **Stocks**: NASDAQ-100 (**Daily Market-Cap-Weighted**)
* **Cryptocurrencies**: Top 20 cryptocurrencies by market capitalization (**Daily Market-Cap-Weighted**)
* **Commodities**: Top 10 commodity futures (**Equal-Weighted**)

Indices are computed daily, reflecting market growth accurately through a daily market-cap weighting. Additionally, the script calculates a **Total Return Index** based on initial portfolio weights (buy-and-hold strategy), allowing for an insightful comparison between dynamic market growth and passive investment returns.

---

## 📌 Project Overview

* **Analysis Period**: January 1, 2019, to present (automatically updated daily)
* **Data Sources**:

  * **Stocks & Commodities**: [Yahoo Finance](https://finance.yahoo.com/)
  * **Cryptocurrencies**: [CoinGecko API](https://www.coingecko.com/api/documentation)
* **Indices Computed**:

  * **Price Index (Daily Market-Cap-Weighted)**: Reflects daily market-price movements with daily re-weighting based on market capitalization.
  * **Total Return Index (Initial Weight, No Rebalancing)**: Cumulative returns calculated based on initial portfolio allocations, representing a buy-and-hold strategy.

---

## 🚀 Quick Start Guide

### Step 1: **Environment Setup**

Install the required Python packages:

```bash
pip install yfinance pandas numpy matplotlib pycoingecko
```

### Step 2: **Run the Script**

Simply run:

```bash
python index_maker.py
```

Upon execution, the script will:

* Generate clear visual comparisons between:

  * **Daily-Weighted Price Indices** and **Total Return Indices** for each asset class.
* Clearly annotate the most recent index values and dates on each plot.
* Display total execution time (typically between 1–3 minutes).

---

## ⚙️ How the Script Works

### ✅ **Automatic Asset Pool Selection**

* **Stocks**: Automatically retrieves current NASDAQ-100 tickers from Wikipedia.
* **Cryptocurrencies**: Retrieves top 20 cryptocurrencies by current market capitalization via CoinGecko API.
* **Commodities**: Utilizes a fixed selection of commonly traded commodity futures tickers from Yahoo Finance.

### ✅ **Data Collection**

* Automatically downloads adjusted daily closing prices for all selected assets using Yahoo Finance.

### ✅ **Initial Portfolio Setup**

* **Stocks**: Calculates initial market capitalization based on outstanding shares data from Yahoo Finance.
* **Cryptocurrencies**: Retrieves initial market caps from CoinGecko API.
* **Commodities**: Assumes equal initial investment (\$100 per commodity).

### ✅ **Index Calculation Methodology**

* **Daily-Weighted Price Index**:

  * Reflects accurate market growth, adjusting market-cap weights every trading day.
* **Total Return Index**:

  * Reflects cumulative returns from initial portfolio weights without any subsequent rebalancing, suitable for evaluating passive investment strategies.

---

## 🔧 Customizing Asset Pools (Optional)

You can manually adjust the ticker symbols for each asset class in the script (`index_maker.py`):

* **Stocks (NASDAQ-100)**:

```python
stock_pool = ["AAPL", "MSFT", "AMZN", "..."]
```

* **Cryptocurrencies**:

```python
crypto_pool = ["BTC-USD", "ETH-USD", "BNB-USD", "..."]
```

* **Commodities**:

```python
commodity_pool = ["GC=F", "CL=F", "SI=F", "..."]
```

Simply modify these lists to customize your analysis according to your requirements.

---

## 🚨 Troubleshooting Common Issues

* **Slow Initial Run**:

  * Initial execution may take a few minutes due to comprehensive data fetching. Subsequent runs typically complete faster.
* **Yahoo Finance Data Download Errors**:

  * Occasionally Yahoo Finance servers may timeout. The script includes retry mechanisms to handle temporary connection issues.
* **CoinGecko API Rate Limits**:

  * If API limits are encountered, consider reducing the number of cryptocurrencies or adding brief pauses between requests.

---

## 📊 Visualizations and Interpretation

The script generates intuitive and detailed visualizations clearly comparing:

* **Solid Lines**: Daily-Weighted Price Indices (Daily Market-Cap Rebalancing)
* **Dashed Lines**: Total Return Indices (Buy-and-Hold, No Rebalancing)

Each plot is clearly annotated with the latest available index value and date, helping you easily track recent market performance.

---

## ⏱ Performance & Execution Time

The script reports the total execution time after completion, typically ranging between **1–3 minutes**:

Example:

```
Total Execution Time: 56.09 seconds
```

---

## 📜 License

This project is licensed under the **MIT License**, allowing you to freely modify, distribute, and reuse the code with proper attribution.

---

**Happy analyzing and investing!** 🚀📊
