# Deployment Notes – BTC Price Aggregator

## Overview
This release includes a command-line tool (main.py) and a validation test suite (test.py) that:

- Fetch live cryptocurrency-to-fiat prices from multiple exchanges.
- Support automatic fiat conversion using CurrencyFreaksConverter.
- Validate exchange implementations and API integrations through unit tests.
- Make it easy to integrate new exchanges and currency converters.

--- 

## Prerequisites

Ensure your environment meets the following requirements:
- Python 3.9+
- Required dependencies:
  ```pip install requests argparse unittest```
- Set the CURRENCY_API_KEY environment variable for fiat conversions.

---

## Core Components

```main.py```
This is the main CLI entry point for fetching and comparing crypto prices across exchanges.

### Usage
```python main.py --crypto BTC --fiat USD```

### Arguments
Flag          Type        Default     Description
`--crypto`	  `Crypto`	  `BTC`	      Cryptocurrency to fetch
`--fiat`	    `Fiat`	    `EUR`	      Fiat currency for price display

### Behaviour
- Initializes all exchange instances (`Binance`, `Kraken`, `Foxbit`).
- Fetches live prices using each exchange’s `get_prices()` implementation.
- Logs prices in ascending order by `actual price`.
- Logs an error if no valid results are returned.

---

```test.py```
Unit tests to ensure:
- Each exchange defines all expected `(Crypto × Fiat)` pairs.
- The `get_prices()` method works or raises controlled exceptions.

### Usage
```
# Checks if the exchanges implementation implement every crypto/fiat pair
python test.py

# Checks every pair, plus run live API tests with 2 seconds delay between calls
python test.py --prices --sleep 2
```

### Arguments
### Flag    Description
`--prices`	Enables real API calls to exchanges
`--sleep`	  Sets delay (in seconds) between API calls to prevent rate limiting, default 0

---

## Expected Behaviour
- `start_exchanges()` instantiates all exchanges correctly.
- Each exchange implements `get_prices()` and defines all valid crypto/fiat pairs.
- Logging works for both main and test runs.
- Unsupported pairs raise `UnsupportedCurrencyError` gracefully.