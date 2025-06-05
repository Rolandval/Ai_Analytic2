from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class InverterTypeEnum(str, Enum):
    hybrid = "hybrid"
    off_line = "off-line"
    online = "online"

class GenerationEnum(str, Enum):
    g1 = 1
    g2 = 2
    g3 = 3
    g4 = 4
    g5 = 5

class InverterCreateSchema(BaseModel):
    full_name: str
    power: float
    inverter_type: InverterTypeEnum
    generation: GenerationEnum
    string_count: int
    brand_id: int
    firmware: str | None = None

class InverterPriceSchema(BaseModel):
    price: float
    inverter_id: int
    supplier_id: int



    
