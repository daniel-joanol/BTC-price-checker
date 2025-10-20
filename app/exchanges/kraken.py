from .exchange import Exchange
from app.domain.currency import Crypto, Fiat
from app.domain.prices import Prices
import requests
from app.utils.logging import setup_logger

log = setup_logger('kraken.py')

pairs = {
  f'{Crypto.BTC.value}-{Fiat.EUR.value}': 'XXBTZEUR',
  f'{Crypto.BTC.value}-{Fiat.USD.value}': 'XXBTZUSD',
  f'{Crypto.BTC.value}-{Fiat.BRL.value}': None,
  f'{Crypto.ETH.value}-{Fiat.EUR.value}': 'XETHZEUR',
  f'{Crypto.ETH.value}-{Fiat.USD.value}': 'XETHZUSD',
  f'{Crypto.ETH.value}-{Fiat.BRL.value}': None,
  f'{Crypto.XMR.value}-{Fiat.EUR.value}': 'XXMRZEUR',
  f'{Crypto.XMR.value}-{Fiat.USD.value}': 'XXMRZUSD',
  f'{Crypto.XMR.value}-{Fiat.BRL.value}': None,
}

class Kraken(Exchange):

  def get_prices(self, crypto: Crypto, fiat: Fiat) -> Prices:
    pair = pairs[f'{crypto.value}-{fiat.value}']
    fiatDoesNotExist = pair == None
    if fiatDoesNotExist:
      pair = pairs[f'{crypto.value}-{Fiat.EUR.value}']

    url=f'https://api.kraken.com/0/public/Ticker?pair={pair}'
    response = requests.get(url)

    if response.status_code == 200:
      return self._set_prices(response.json(), fiatDoesNotExist, fiat)

    else:
      log.error(f'Petition failed: {response.status_code}')
      log.error(f'Response: {response.json()}')

    
  def _set_prices(self, data: dict, fiatDoesNotExist: bool, fiat: Fiat) -> Prices:
    exchange='Kraken'
    pair_key = list(data['result'].keys())[0]
    pair_data = data['result'][pair_key]
    actual = float(pair_data['c'][0])
    higher = float(pair_data['h'][1])
    lower = float(pair_data['l'][1])
    open_price = float(pair_data['o'])
    percentage_change = ((actual - open_price) / open_price) * 100

    if fiatDoesNotExist:
      rate = 1
      return Prices(
        exchange, 
        actual=self._convert(actual, rate),
        higher=self._convert(higher, rate),
        lower=self._convert(lower, rate),
        percentage_change=self._convert(percentage_change, rate)
      )
    
    else:
      return Prices(exchange, actual, higher, lower, percentage_change)
    

  def _convert(self, value: float, rate: float) -> float:
    return value * rate