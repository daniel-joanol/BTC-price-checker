from .exchange import Exchange
from app.domain.currency import Crypto, Fiat
from app.domain.prices import Prices
from app.exception.exceptions import UnsupportedCurrencyError, PetitionError
from app.converter.currency_freaks_converter import CurrencyFreaksConverter
from app.util.logging import setup_logger
import requests

log = setup_logger('foxbit.py')
DEFAULT_FIAT = Fiat.BRL
DELISTED = 'DELISTED'

class Foxbit(Exchange):
    
  pairs = {
    f'{Crypto.BTC.value}-{Fiat.EUR.value}': None,
    f'{Crypto.BTC.value}-{Fiat.USD.value}': 'btcusdt',
    f'{Crypto.BTC.value}-{Fiat.BRL.value}': 'btcbrl',
    f'{Crypto.ETH.value}-{Fiat.EUR.value}': None,
    f'{Crypto.ETH.value}-{Fiat.USD.value}': 'ethusdt',
    f'{Crypto.ETH.value}-{Fiat.BRL.value}': 'ethbrl',
    f'{Crypto.XMR.value}-{Fiat.EUR.value}': DELISTED,
    f'{Crypto.XMR.value}-{Fiat.USD.value}': DELISTED,
    f'{Crypto.XMR.value}-{Fiat.BRL.value}': DELISTED
  }
    
  def __init__(self, converter: CurrencyFreaksConverter):
    self.converter = converter
        
        
  def get_prices(self, crypto: Crypto, fiat: Fiat) -> Prices:
    pair = self.pairs[f'{crypto.value}-{fiat.value}']
        
    if pair == DELISTED:
      log.info('This pair have been delisted')
      raise UnsupportedCurrencyError()
        
    fiat_does_not_exist = pair == None
    if fiat_does_not_exist:
      pair = self.pairs[f'{crypto.value}-{DEFAULT_FIAT.value}']
            
    url = f'https://api.foxbit.com.br/rest/v3/markets/ticker/24hr'
    response = requests.get(url)
        
    if response.status_code == 200:
      return self._set_prices(response.json(), fiat_does_not_exist, fiat, pair)      
      
    else:
      log.error(f'Petition failed: {response.status_code}')
      log.error(f'Response: {response.json()}')
      raise PetitionError()
        
        
  def _set_prices(self, data: dict, fiat_does_not_exist: bool, convert_to: Fiat, pair: str) -> Prices:
    all_values = list(data['data'])
    found = False
    for values in all_values:
      found = values['market_symbol'] == pair
      
      if found:
        exchange = 'Foxbit'
        actual = float(values['last_trade']['price'])
        rolling_24 = values['rolling_24h']
        higher = float(rolling_24['high'])
        lower = float(rolling_24['low'])
        percentage_change = float(rolling_24['price_change_percent'])
        
        if fiat_does_not_exist:
          rate = self.converter.get_conversion_rate(DEFAULT_FIAT, convert_to)
          return Prices(
            exchange,
            actual=self._convert(actual, rate),
            higher=self._convert(higher, rate),
            lower=self._convert(lower, rate),
            percentage_change=percentage_change
          )
          
        else:
          return Prices(exchange, actual, higher, lower, percentage_change)
        
    if not found:
      log.error(f'Pair {pair} not found on response')
      raise UnsupportedCurrencyError()
  
  
  def _convert(self, value: float, rate: float) -> float:
    return value * rate
            

            