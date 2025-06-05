from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class PanelTypeEnum(str, Enum):
    first_side = "Одностороння"
    second_side = "Двостороння"


class CellTypeEnum(str, Enum):
    n_type = "n-type"
    p_type = "p-type"


class SolarPanelCreateSchema(BaseModel):
    full_name: str
    power: float
    panel_type: PanelTypeEnum
    cell_type: CellTypeEnum
    thickness: float
    brand_id: int

class SolarPanelPriceSchema(BaseModel):
    price: float
    solar_panel_id: int
    supplier_id: int



    
