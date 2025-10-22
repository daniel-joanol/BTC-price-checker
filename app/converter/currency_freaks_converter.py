import os
import requests
from .currency_converter import CurrencyConverter
from app.domain.currency import Fiat
from app.utils.logging import setup_logger

log = setup_logger('currency_freaks_converter.py')

CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')

class CurrencyFreaksConverter(CurrencyConverter):

  def get_conversion_rate(convert_from: Fiat, convert_to: Fiat) -> float:
    url = f'https://api.currencyfreaks.com/v2.0/rates/latest?apikey={CURRENCY_API_KEY}&symbols={convert_from.value}'
    response = requests.get(url)
    print(f'{response.json()}')
    return None