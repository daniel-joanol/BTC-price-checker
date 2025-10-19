# BTC-price-checker

A lightweight Python tool to fetch and compare live cryptocurrency prices — including **Binance**, **Kraken**, and **Foxbit** — with key market metrics like **24h high, low, and percentage change**.

---

## 🚀 Features

- ✅ Fetch real-time Bitcoin price from:
  - [Binance](https://api.binance.com/)
  - [Kraken](https://api.kraken.com/)
  - [Foxbit](https://foxbit.com.br/)
- 📊 Show last trade, 24h high/low, and price change percentage
- 💱 Compare prices across exchanges
- 🔁 Optional auto-refresh for live updates
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
