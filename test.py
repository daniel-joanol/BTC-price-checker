import unittest, logging
from main import start_exchanges
from app.utils.logging import setup_logger;
from app.domain.currency import Fiat, Crypto

log = setup_logger('test.py', logging.DEBUG)

class TestExchanges(unittest.TestCase):
    
    def test_pairs(self):
        exchanges = start_exchanges()
        required_pairs = len(Fiat) * len(Crypto)
        log.debug(f'Every exchange must have exactly {required_pairs} pairs defined')
        for exchange in exchanges:
            exchange_pairs = len(exchange.pairs)
            self.assertEqual(required_pairs, exchange_pairs)
    
if __name__ == '__main__':
    unittest.main()