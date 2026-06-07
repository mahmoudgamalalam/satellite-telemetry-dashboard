from sqlalchemy import Column, Integer, String, Float
from .database import Base


class TelemetryRecord(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)

    satellite_id = Column(String)
    battery = Column(Float)
    temperature = Column(Float)
    signal_strength = Column(Float)
    status = Column(String)

    alerts = Column(String)
    timestamp = Column(String)