import argparse
from app.domain.currency import Fiat, Crypto
from app.domain.prices import Prices
from app.exchange.exchange import Exchange
from app.exchange.binance import Binance
from app.exchange.kraken import Kraken
from app.converter.currency_freaks_converter import CurrencyFreaksConverter
from app.exception.exceptions import PetitionError, UnsupportedCurrencyError
from typing import Optional
from app.util.logging import setup_logger

log = setup_logger('main.py')

def start_exchanges():
  converter = CurrencyFreaksConverter()
  return [Binance(), Kraken(converter)]

def get_prices(exchange: Exchange, crypto: Crypto, fiat: Fiat) -> Optional[Prices]:
  try:
    return exchange.get_prices(crypto, fiat)
  except PetitionError as e:
    pass
  except UnsupportedCurrencyError as e:
    pass
  except Exception as e:
    log.error(f'{e}')
    pass


def main(crypto: Crypto, fiat: Fiat):
  log.info(f'crypto: {crypto.value} / fiat: {fiat.value}')
  price_list = list()
  exchanges = start_exchanges()
  for exchange in exchanges:
    prices = get_prices(exchange, crypto, fiat)
    if prices != None:
      price_list.append(prices)

  if price_list == []:
    log.error('There are no results to show')
  else:
    sorted_list = sorted(price_list, key=lambda p: p.actual)
    for prices in sorted_list:
      log.info(f'{prices}')
    

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=
    """
    A lightweight Python tool to fetch and compare live cryptocurrency prices.
    Set the environment variable CURRENCY_API_KEY to enable automatic conversion when certain fiat currencies are not available on an exchange.
    Specify the cryptocurrency to fetch and the fiat currency for price calculation.
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("--crypto", type=Crypto, required=False, default=Crypto.BTC, help="Default value: BTC")
  parser.add_argument("--fiat", type=Fiat, required=False, default=Fiat.EUR, help="Defautl value: EUR")
  
  args = parser.parse_args()
  main(args.crypto, args.fiat)