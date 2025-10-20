from abc import ABC, abstractmethod
from ..domain.prices import Prices
from ..domain.currency import Crypto, Fiat

class Exchange(ABC):

  @abstractmethod
  def get_prices(self, crypto:Crypto, fiat:Fiat) -> Prices:
    ...