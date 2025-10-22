from abc import ABC, abstractmethod
from ..domain.prices import Prices
from ..domain.currency import Crypto, Fiat

class Exchange(ABC):
  pairs: map

  @abstractmethod
  def get_prices(self, crypto:Crypto, fiat:Fiat) -> Prices:
    ...
    
  def __init_subclass__(cls):
    if not hasattr(cls, 'pairs'):
      raise TypeError(f"{cls.__name__} must define a map of 'pairs'")