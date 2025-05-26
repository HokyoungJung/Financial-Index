# Market-Cap-Weighted Indices (Stocks, Crypto, Commodities)

This project provides an automated, daily-updated calculation of market-cap-weighted indices for three asset classes:

* **Stocks**: NASDAQ-100
* **Cryptocurrencies**: Top 20 cryptocurrencies by market capitalization
* **Commodities**: Top 10 commodity futures (equal-weighted, fixed list)

The indices are calculated on a daily basis with monthly rebalancing, reflecting realistic market practices.

---

## 📌 Project Overview

* **Time Period**: January 1, 2019, to today (automatically updates)
* **Data Sources**:

  * Stocks and commodities: [Yahoo Finance](https://finance.yahoo.com/)
  * Cryptocurrencies: [CoinGecko API](https://www.coingecko.com/api/documentation)
* **Calculation Methodology**:

  * Daily index calculation (accurate daily tracking)
  * Monthly rebalancing (reflecting real-world practices)

---

## 🚀 Quick Start

### 1. **Setup Environment**

```bash
pip install yfinance pandas numpy matplotlib pycoingecko
```

### 2. **Run the Python Script**

```bash
python index_maker.py
```

After execution, you will see plotted indices for:

* NASDAQ-100 stocks (Market Cap Weighted)
* Top 20 cryptocurrencies (Market Cap Weighted)
* Top 10 commodities (Equal Weighted)

The script will also display the total execution time.

---

## ⚙️ How the Script Works

### Automatic Asset Pool Updates:

* **Stocks**: Retrieves NASDAQ-100 tickers automatically from Wikipedia.
* **Cryptocurrencies**: Fetches the top 20 cryptocurrencies by market cap using CoinGecko API.
* **Commodities**: Uses a fixed pool of the top 10 most liquid commodity futures from Yahoo Finance.

### Daily Data Collection:

* Downloads daily adjusted closing prices for each asset from Yahoo Finance.

### Initial Market Cap and Units Setup:

* **Stocks**: Obtains shares outstanding to calculate market caps.
* **Cryptocurrencies**: Uses CoinGecko API to fetch current market caps for initial unit calculation.
* **Commodities**: Sets an equal initial investment (\$100 each).

### Index Calculation:

* Daily index calculation with returns computed each trading day.
* Rebalances indices weights only at the end of each month.

---

## 🛠 Manual Adjustments of Tickers

If you wish to manually adjust the tickers for each asset class, you can easily modify the lists in the script:

* **Stocks** (NASDAQ-100):

  ```python
  # Modify the NASDAQ-100 tickers manually if needed
  stock_pool = ["AAPL", "MSFT", "AMZN", ...]
  ```

* **Cryptocurrencies**:

  ```python
  # Manually set your preferred cryptocurrencies
  crypto_pool = ["BTC-USD", "ETH-USD", "BNB-USD", ...]
  ```

* **Commodities**:

  ```python
  # Manually set commodity tickers
  commodity_pool = ["GC=F", "CL=F", "SI=F", ...]
  ```

Simply replace the existing ticker lists with your desired selections.

---

## 🚨 Common Issues and Troubleshooting

* **Execution Time**:
  Running the script for the first time may take several minutes due to data downloading. Subsequent runs will be faster.

* **Ticker Changes**:
  Yahoo Finance occasionally updates ticker symbols. If you encounter errors or missing data, verify ticker symbols on Yahoo Finance.

* **CoinGecko API Limitations**:
  Free CoinGecko API usage is generally sufficient, but if you experience rate-limiting, consider requesting fewer cryptocurrencies or adding delays between API requests.

---

## 📊 Output and Visualization

The script generates clear visual plots for each asset class index, enabling intuitive analysis of market trends.

### Example Output:

* NASDAQ-100 Market Cap Weighted Index (blue)
* Cryptocurrencies Top 20 Market Cap Index (purple)
* Commodities Top 10 Equal-Weighted Index (green)

---

## ⏱ Performance

The total execution time of the script is displayed upon completion. Typically, the execution time ranges from **1 to 3 minutes**, depending on your internet speed and computing power.

Example:

```
Total Execution Time: 128.45 seconds
```

---

## 📜 License

This project is provided under the MIT License. You are free to modify, distribute, and use this script in your own projects with attribution.

---

**Enjoy analyzing your custom market-cap-weighted indices!**
