# 📈 Market-Cap Weighted Indices

This project provides an automated calculation and visualization of market-cap-weighted indices and total return indices for three asset classes:

* **Stocks**: NASDAQ-100 (Market Cap Weighted)
* **Cryptocurrencies**: Top 20 cryptocurrencies by market capitalization (Market Cap Weighted)
* **Commodities**: Top 10 commodity futures (Equal Weighted)

Indices are computed **daily** with **monthly rebalancing**, reflecting realistic and professional financial analysis practices. The script also calculates and visualizes cumulative return indices, enabling easy comparisons between rebalanced and buy-and-hold strategies.

---

## 📌 Project Overview

* **Time Period**: January 1, 2019, to the present (automatically updated)
* **Data Sources**:

  * Stocks and Commodities: [Yahoo Finance](https://finance.yahoo.com/)
  * Cryptocurrencies: [CoinGecko API](https://www.coingecko.com/api/documentation)
* **Index Calculation**:

  * **Price Index**: Daily returns calculated with monthly rebalancing.
  * **Total Return Index**: Daily cumulative returns calculated from initial portfolio weights without rebalancing.

---

## 🚀 Quick Start Guide

### Step 1: **Set Up the Environment**

```bash
pip install yfinance pandas numpy matplotlib pycoingecko
```

### Step 2: **Run the Script**

```bash
python index_maker.py
```

Upon completion, the script will:

* Generate clear visual plots comparing Price Indices and Return Indices for:

  * NASDAQ-100 stocks
  * Top 20 cryptocurrencies
  * Top 10 commodities
* Print the total execution time (usually **1–3 minutes**).

---

## ⚙️ How the Script Works

### Automatic Asset Selection

* **Stocks**: Retrieves NASDAQ-100 tickers automatically from Wikipedia.
* **Cryptocurrencies**: Fetches top 20 cryptocurrencies by market capitalization from CoinGecko.
* **Commodities**: Uses a fixed list of popular commodity futures from Yahoo Finance.

### Daily Data Collection

* Automatically downloads adjusted daily closing prices for each asset.

### Initial Portfolio Setup

* **Stocks**: Calculates initial market caps based on outstanding shares.
* **Cryptocurrencies**: Retrieves market caps via CoinGecko API for accurate weighting.
* **Commodities**: Allocates equal initial investment (\$100 per commodity).

### Index Calculation Methodology

* **Daily Price Index**:

  * Reflects daily market-price movements with monthly rebalancing.
* **Total Return Index**:

  * Computes cumulative daily returns, reflecting a buy-and-hold strategy without rebalancing.

---

## 🔧 Customizing Asset Pools

You can manually adjust the tickers for each asset class directly in the script (`index_maker.py`):

* **Stocks (NASDAQ-100)**:

```python
# Example modification
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

Simply replace or update these lists with your desired assets.

---

## 🚨 Troubleshooting Common Issues

* **Slow Initial Run**:

  * The initial execution may take several minutes due to extensive data downloading. Subsequent runs will be faster.
* **Ticker Updates**:

  * Occasionally, Yahoo Finance updates ticker symbols. Verify ticker symbols on [Yahoo Finance](https://finance.yahoo.com/) if data issues occur.
* **CoinGecko API Limits**:

  * If you encounter API limits, consider reducing the number of cryptocurrencies or adding delays between requests.

---

## 📊 Visualization and Interpretation

The script generates intuitive visual plots:

* **Solid lines**: Price Indices (Monthly Rebalancing)
* **Dashed lines**: Total Return Indices (No Rebalancing)

These visualizations help illustrate the performance differences between active rebalancing strategies and passive investment approaches.

---

## ⏱ Performance & Execution Time

The script measures and displays its total execution time upon completion, typically ranging from **1–3 minutes**.

Example:

```
Total Execution Time: 57.73 seconds
```

---

## 📜 License

This project is distributed under the **MIT License**. You are free to modify, distribute, and reuse the code with proper attribution.

---

## 🙌 Contributions

Improvements and contributions are welcome! Feel free to open issues or submit pull requests directly through GitHub.

---

**Happy analyzing and investing!** 📊🚀
