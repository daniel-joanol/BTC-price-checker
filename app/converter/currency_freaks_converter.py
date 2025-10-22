import os
import requests
from .currency_converter import CurrencyConverter
from app.domain.currency import Fiat
from app.exception.exceptions import PetitionError
from app.utils.logging import setup_logger

log = setup_logger('currency_freaks_converter.py')

CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')

class CurrencyFreaksConverter(CurrencyConverter):

  def get_conversion_rate(self, convert_from: Fiat, convert_to: Fiat) -> float:
    url = f'https://api.currencyfreaks.com/v2.0/rates/latest?apikey={CURRENCY_API_KEY}&symbols={convert_from.value},{convert_to.value}'
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
      rate_from = float(data['rates'][convert_from.value])
      rate_to = float(data['rates'][convert_to.value])
      return rate_to / rate_from
    
    else:
      log.error(f'Petition failed: {response.status_code}')
      log.error(f'Petition response: {response.json()}')
      raise PetitionError()