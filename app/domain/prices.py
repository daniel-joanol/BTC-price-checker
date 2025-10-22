from dataclasses import dataclass
from typing import Optional

@dataclass
class Prices:
  exchange: str
  actual: float
  higher: Optional[float] = None
  lower: Optional[float] = None
  percentage_change: Optional[float] = None
