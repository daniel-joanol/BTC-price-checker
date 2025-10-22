from .exchange import Exchange
from app.domain.currency import Crypto, Fiat
from app.domain.prices import Prices
from app.exception.exceptions import UnsupportedCurrencyError, PetitionError
import requests
from app.utils.logging import setup_logger

log = setup_logger('binance.py')

DELISTED = 'DELISTED'
pairs = {
  f'{Crypto.BTC.value}-{Fiat.EUR.value}': 'BTCEUR',
  f'{Crypto.BTC.value}-{Fiat.USD.value}': 'BTCUSDT',
  f'{Crypto.BTC.value}-{Fiat.BRL.value}': 'BTCBRL',
  f'{Crypto.ETH.value}-{Fiat.EUR.value}': 'ETHEUR',
  f'{Crypto.ETH.value}-{Fiat.USD.value}': 'ETHUSDT',
  f'{Crypto.ETH.value}-{Fiat.BRL.value}': 'ETHBRL',
  f'{Crypto.XMR.value}-{Fiat.EUR.value}': DELISTED,
  f'{Crypto.XMR.value}-{Fiat.USD.value}': DELISTED,
  f'{Crypto.XMR.value}-{Fiat.BRL.value}': DELISTED
}

class Binance(Exchange):
  
  def get_prices(self, crypto: Crypto, fiat: Fiat) -> Prices:
    pair = pairs[f'{crypto.value}-{fiat.value}']
    if pair == DELISTED:
      log.info('This pair have been delisted')
      raise UnsupportedCurrencyError()

    url = f'https://api.binance.com/api/v3/ticker/24hr?symbol={pair}'
    response = requests.get(url)

    if response.status_code == 200:
      return self._set_prices(response.json())

    else:
      log.error(f'Petition failed: {response.status_code}')
      log.error(f'Response: {response.json()}')
      raise PetitionError()

  
  def _set_prices(self, data: dict) -> Prices:
    return Prices(
      exchange='Binance',
      actual=float(data['lastPrice']),
      higher=float(data['highPrice']),
      lower=float(data['lowPrice']),
      percentage_change=float(data['priceChangePercent'])
    )  
  
