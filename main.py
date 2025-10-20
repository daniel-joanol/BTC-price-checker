import argparse
from app.domain.currency import Fiat, Crypto
from app.exchanges.binance import Binance
from app.exchanges.kraken import Kraken
from app.utils.logging import setup_logger

log = setup_logger('main.py')

def start_exchanges():
  return Binance(), Kraken()


def main(crypto: Crypto, fiat: Fiat):
  log.info(f'crypto: {crypto.value} / fiat: {fiat.value}')
  binance, kraken = start_exchanges()
  price_list = [
    binance.get_prices(crypto, fiat),
    kraken.get_prices(crypto, fiat)
  ]
  sorted_list = sorted(price_list, key=lambda p: p.actual)
  for prices in sorted_list:
    log.info(f'{prices}')
    

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Choose the crypto currency you want to search for and the fiat currency in which the prices should be calculated.")
  parser.add_argument("--crypto", type=Crypto, required=False, default=Crypto.BTC, help="Default value: BTC")
  parser.add_argument("--fiat", type=Fiat, required=False, default=Fiat.EUR, help="Defautl value: EUR")
  
  args = parser.parse_args()
  main(args.crypto, args.fiat)