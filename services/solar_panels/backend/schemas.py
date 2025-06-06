from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PanelColorEnum(str, Enum):
    default = "Default"
    all_black = "All_Black"
    

class FrameColorEnum(str, Enum):
    silver = "Silver"
    black = "Black"
    

class PanelTypeEnum(str, Enum):
    first_side = "одностороння"
    second_side = "двостороння"


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
    panel_color: PanelColorEnum
    frame_color: FrameColorEnum

class SolarPanelPriceSchema(BaseModel):
    price: float
    solar_panel_id: int
    supplier_id: int



    
