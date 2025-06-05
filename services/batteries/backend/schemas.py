from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class RegionEnum(str, Enum):
    EUROPE = "EUROPE"
    ASIA = "ASIA"

class ElectrolyteEnum(str, Enum):
    LAB = "LAB"
    AGM = "AGM"
    GEL = "GEL"
    EFB = "EFB"

class BatteryCreateSchema(BaseModel):
    full_name: str
    c_amps: int
    region: RegionEnum
    polarity: str
    electrolyte: ElectrolyteEnum
    brand_id: int

class BatteryPriceSchema(BaseModel):
    price: float
    battery_id: int
    supplier_id: int



    
