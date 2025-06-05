from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class SupplierStatus(Base):
    __tablename__ = "supplier_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # ORM-зв'язки
    batteries_suppliers = relationship("BatteriesSuppliers", back_populates="status")
    inverters_suppliers = relationship("InvertersSuppliers", back_populates="status")
    solar_panels_suppliers = relationship("SolarPanelsSuppliers", back_populates="status")

class Batteries(Base):
    __tablename__ = "batteries"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    c_amps = Column(Integer, nullable=False, default=0)
    volume = Column(Float, nullable=True, default=0)
    region = Column(String, nullable=False, default="EUROPE")
    polarity = Column(String, nullable=False, default="R+")
    electrolyte = Column(String, nullable=False, default="LAB")

    brand_id = Column(Integer, ForeignKey('batteries_brands.id'), nullable=True)    

    # ORM-зв'язки
    brand = relationship("BatteriesBrands", back_populates="batteries")
    prices = relationship("BatteriesPrices", back_populates="battery", cascade="all, delete-orphan")
    prices_current = relationship("BatteriesPricesCurrent", back_populates="battery", cascade="all, delete-orphan")


class BatteriesBrands(Base):
    __tablename__ = "batteries_brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # ORM-зв'язки
    batteries = relationship("Batteries", back_populates="brand")


class BatteriesSuppliers(Base):
    __tablename__ = "batteries_suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status_id = Column(Integer, ForeignKey('supplier_status.id'), nullable=True)

    
    # ORM-зв'язки
    status = relationship("SupplierStatus", back_populates="batteries_suppliers")
    prices = relationship("BatteriesPrices", back_populates="supplier")
    prices_current = relationship("BatteriesPricesCurrent", back_populates="supplier")


class BatteriesPrices(Base):
    __tablename__ = "batteries_prices"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
    battery_id = Column(Integer, ForeignKey('batteries.id'), nullable=True)
    supplier_id = Column(Integer, ForeignKey('batteries_suppliers.id'), nullable=True)
    
    # ORM-зв'язки
    battery = relationship("Batteries", back_populates="prices")
    supplier = relationship("BatteriesSuppliers", back_populates="prices")


class BatteriesPricesCurrent(Base):
    __tablename__ = "batteries_prices_current"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
    
    battery_id = Column(Integer, ForeignKey('batteries.id'), nullable=True)
    supplier_id = Column(Integer, ForeignKey('batteries_suppliers.id'), nullable=True)
    
    # ORM-зв'язки
    battery = relationship("Batteries", back_populates="prices_current")
    supplier = relationship("BatteriesSuppliers", back_populates="prices_current")




class SolarPanels(Base):
    __tablename__ = "solar_panels"

    id = Column(Integer, primary_key=True, index=True)
    power = Column(Float, nullable=False)
    full_name = Column(String, nullable=False)
    panel_type = Column(String, nullable=False, default="одностороння")
    cell_type = Column(String, nullable=False, default="n-type")
    thickness = Column(Float, nullable=False, default=30)
    
    brand_id = Column(Integer, ForeignKey('solar_panels_brands.id'), nullable=True)
    
    # ORM-зв'язки
    brand = relationship("SolarPanelsBrands", back_populates="solar_panels")
    prices = relationship("SolarPanelsPrices", back_populates="panel", cascade="all, delete-orphan")
    prices_current = relationship("SolarPanelsPricesCurrent", back_populates="panel", cascade="all, delete-orphan")


class SolarPanelsBrands(Base):
    __tablename__ = "solar_panels_brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # ORM-зв'язки
    solar_panels = relationship("SolarPanels", back_populates="brand")


class SolarPanelsSuppliers(Base):
    __tablename__ = "solar_panels_suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status_id = Column(Integer, ForeignKey('supplier_status.id'), nullable=True)
    
    # ORM-зв'язки
    status = relationship("SupplierStatus", back_populates="solar_panels_suppliers")
    prices = relationship("SolarPanelsPrices", back_populates="supplier")
    prices_current = relationship("SolarPanelsPricesCurrent", back_populates="supplier")


class SolarPanelsPrices(Base):
    __tablename__ = "solar_panels_prices"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
    panel_id = Column(Integer, ForeignKey('solar_panels.id'), nullable=True)
    supplier_id = Column(Integer, ForeignKey('solar_panels_suppliers.id'), nullable=True)
    
    # ORM-зв'язки
    panel = relationship("SolarPanels", back_populates="prices")
    supplier = relationship("SolarPanelsSuppliers", back_populates="prices")



class SolarPanelsPricesCurrent(Base):
    __tablename__ = "solar_panels_prices_current"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
    
    panel_id = Column(Integer, ForeignKey('solar_panels.id'), nullable=True)
    supplier_id = Column(Integer, ForeignKey('solar_panels_suppliers.id'), nullable=True)
    
    # ORM-зв'язки
    panel = relationship("SolarPanels", back_populates="prices_current")
    supplier = relationship("SolarPanelsSuppliers", back_populates="prices_current")



class Inverters(Base):
    __tablename__ = "inverters"

    id = Column(Integer, primary_key=True, index=True)
    power = Column(Float, nullable=False)
    full_name = Column(String, nullable=False)
    inverter_type = Column(String, nullable=False, default="gybrid")
    generation = Column(String, nullable=False, default="4")
    string_count = Column(Integer, nullable=False, default=0)
    firmware = Column(String, nullable=True)
    
    brand_id = Column(Integer, ForeignKey('inverters_brands.id'), nullable=True)
    
    # ORM-зв'язки
    brand = relationship("InvertersBrands", back_populates="inverters")
    prices = relationship("InvertersPrices", back_populates="inverter", cascade="all, delete-orphan")
    prices_current = relationship("InvertersPricesCurrent", back_populates="inverter", cascade="all, delete-orphan")


class InvertersBrands(Base):
    __tablename__ = "inverters_brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # ORM-зв'язки
    inverters = relationship("Inverters", back_populates="brand")


class InvertersSuppliers(Base):
    __tablename__ = "inverters_suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status_id = Column(Integer, ForeignKey('supplier_status.id'), nullable=True)
    
    # ORM-зв'язки
    status = relationship("SupplierStatus", back_populates="inverters_suppliers")
    prices = relationship("InvertersPrices", back_populates="supplier")
    prices_current = relationship("InvertersPricesCurrent", back_populates="supplier")


class InvertersPrices(Base):
    __tablename__ = "inverters_prices"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
    inverter_id = Column(Integer, ForeignKey('inverters.id'), nullable=True)
    supplier_id = Column(Integer, ForeignKey('inverters_suppliers.id'), nullable=True)
    
    # ORM-зв'язки
    inverter = relationship("Inverters", back_populates="prices")
    supplier = relationship("InvertersSuppliers", back_populates="prices")


class InvertersPricesCurrent(Base):
    __tablename__ = "inverters_prices_current"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
    
    inverter_id = Column(Integer, ForeignKey('inverters.id'), nullable=True)
    supplier_id = Column(Integer, ForeignKey('inverters_suppliers.id'), nullable=True)
    
    # ORM-зв'язки
    inverter = relationship("Inverters", back_populates="prices_current")
    supplier = relationship("InvertersSuppliers", back_populates="prices_current")

