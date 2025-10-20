# BTC-price-checker

A lightweight Python tool to fetch and compare live cryptocurrency prices — from exchanges like **Binance**, **Kraken**, and **Foxbit** — with key market metrics like **24h high, low, actual price and price percentage change**.

---

## 🚀 Features

- ✅ Fetch real-time Bitcoin price from:
  - [Binance](https://api.binance.com/)
  - [Kraken](https://api.kraken.com/)
  - [Foxbit](https://foxbit.com.br/)
- 📊 Show last trade, 24h high/low, actual price and price change percentage
- 💱 Compare prices across exchanges
- 🧩 Easy to extend with more coins or exchanges

---

## 🧠 How It Works

Each exchange has a public REST API endpoint for market data.  
This script pulls the relevant fields and normalizes them into a comparable format.

| Exchange | Endpoint | Data |
|-----------|-----------|------|
| Binance | `https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT` | `lastPrice`, `highPrice`, `lowPrice`, `priceChangePercent` |
| Kraken | `https://api.kraken.com/0/public/Ticker?pair=XBTUSDT` | `c[0]`, `h[1]`, `l[1]` |
| Foxbit | `https://api.foxbit.com.br/rest/v3/market/ticker?symbol=btcbrl` | `last_trade.price`, `rolling_24h.high`, `rolling_24h.low`, `rolling_24h.price_change_percent` |

---

## ⚔️ Challenges & Solutions

### Currency normalization for Foxbit
Foxbit only provides prices in BRL. To compare it with other exchanges using the same currency, the script uses Currency Freaks.

### Price change percentage for Kraken
Kraken’s API doesn’t directly provide the 24h price change percentage. The script calculates it manually using the formula:

### Data normalization across APIs
Each exchange provides slightly different field names and formats. The script standardizes them into a consistent structure for easy comparison.

### Extensibility
The architecture allows you to add new exchanges or cryptocurrencies with minimal code changes.

