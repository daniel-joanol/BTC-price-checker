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
    Test if the the exchanges implement every pair and if they can get the prices.
    The calls to get prices may be paid, which could make the test expansive, or they could be free and limited, which could interfere with the main script.
    For these reasons the flag --sleep is optional.
    There's a second parameter called --sleep, which sets the sleep time between api calls.
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('--prices', action='store_true', help='make real calls to the APIs')
  parser.add_argument('--sleep', type=int, default=0, help='default value: 0')
  args = parser.parse_args()
  print(args)
  unittest.main(argv=[sys.argv[0]])