import argparse
from app.domain.currency import Fiat, Crypto
from app.domain.prices import Prices
from app.exchanges.binance import Binance
from app.utils.logging import setup_logger

log = setup_logger('main.py')

def start_exchanges():
  binance = Binance()
  return binance


def main(crypto: Crypto, fiat: Fiat):
  log.info(f'crypto: {crypto.value} / fiat: {fiat.value}')
  binance = start_exchanges()
  binancePrices = binance.get_prices(crypto, fiat)
  log.info(f'{binancePrices}')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Choose the crypto currency you want to search for and the fiat currency in which the prices should be calculated.")
  parser.add_argument("--crypto", type=Crypto, required=False, default=Crypto.BTC, help="Default value: BTC")
  parser.add_argument("--fiat", type=Fiat, required=False, default=Fiat.EUR, help="Defautl value: EUR")
  
  args = parser.parse_args()
  main(args.crypto, args.fiat)