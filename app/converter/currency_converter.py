from abc import ABC, abstractmethod
from ..domain.currency import Fiat

class CurrencyConverter(ABC):

  @abstractmethod
  def get_conversion_rate(convert_from: Fiat, convert_to: Fiat) -> float:
    ...