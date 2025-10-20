from dataclasses import dataclass
from typing import Optional
from .currency import Fiat

@dataclass
class Prices:
  exchange: str
  actual: float
  higher: Optional[float] = None
  lower: Optional[float] = None
  percentageChange: Optional[float] = None
