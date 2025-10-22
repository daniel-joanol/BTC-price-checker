import unittest, logging, argparse, sys, time
from main import start_exchanges
from app.util.logging import setup_logger;
from app.domain.currency import Fiat, Crypto
from app.exception.exceptions import UnsupportedCurrencyError

log = setup_logger('test.py', logging.DEBUG)

class TestExchanges(unittest.TestCase):
  
  exchanges = start_exchanges()
    
  def test_pairs(self):
    required_pairs = len(Fiat) * len(Crypto)
    log.debug(f'Every exchange must have exactly {required_pairs} pairs defined')
    for exchange in self.exchanges:
      exchange_pairs = len(exchange.pairs)
      self.assertEqual(required_pairs, exchange_pairs)
            
            
  def test_prices(self):
    log.debug(f'Flag --prices is set as {args.prices}')
    if args.prices:
      for exchange in self.exchanges:
        for crypto in list(Crypto):
          for fiat in list(Fiat):
            try:
              log.debug(f'{exchange.__class__.__name__} {crypto.value} {fiat.value}')
              time.sleep(args.sleep)
              exchange.get_prices(crypto, fiat)
              log.debug('ok')
              self.assertTrue(True)
            except UnsupportedCurrencyError as e:
              self.assertTrue(True)
            except Exception as e:
              log.debug(f'{e}')
              self.assertTrue(False)
    
    
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="""
    Test whether the exchanges implement all expected currency pairs and whether they can retrieve real-time prices.

    Calling the actual price APIs may incur costs or be subject to rate limits, which could interfere with normal usage. 
    To prevent unintended behavior or extra charges, the --prices flag must be explicitly set to enable live API calls.

    An optional --sleep parameter sets a delay (in seconds) between each API call. Default is 0.
    """, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('--prices', action='store_true', help='make real API calls to fetch prices')
  parser.add_argument('--sleep', type=int, default=0, help='sleep time (in seconds) between API calls; default: 0')
  
  args = parser.parse_args()
  unittest.main(argv=[sys.argv[0]])