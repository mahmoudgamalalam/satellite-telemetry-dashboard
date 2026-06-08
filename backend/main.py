
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from .database import SessionLocal, engine, Base
from .models import TelemetryRecord

app = FastAPI()

Base.metadata.create_all(bind=engine)


class Telemetry(BaseModel):
    satellite_id: str
    battery: float
    temperature: float
    signal_strength: float
    status: str


def check_alerts(data: Telemetry):
    alerts = []

    if data.battery < 20:
        alerts.append("LOW BATTERY")

    if data.temperature > 40:
        alerts.append("HIGH TEMPERATURE")

    if data.signal_strength < -90:
        alerts.append("WEAK SIGNAL")

    return alerts


@app.get("/")
def home():
    return {"message": "Satellite Telemetry API is running"}


@app.post("/telemetry")
def receive_telemetry(data: Telemetry):
    alerts = check_alerts(data)

    db = SessionLocal()

    record = TelemetryRecord(
        satellite_id=data.satellite_id,
        battery=data.battery,
        temperature=data.temperature,
        signal_strength=data.signal_strength,
        status=data.status,
        alerts=",".join(alerts),
        timestamp=datetime.utcnow().isoformat()
    )

    db.add(record)
    db.commit()
    db.close()

    return {
        "message": "Telemetry received",
        "alerts": alerts
    }


@app.get("/telemetry/latest")
def get_latest_telemetry():
    db = SessionLocal()

    latest = db.query(TelemetryRecord).order_by(TelemetryRecord.id.desc()).first()

    db.close()

    if latest is None:
        return {"message": "No telemetry received yet"}

    return {
        "timestamp": latest.timestamp,
        "data": {
            "satellite_id": latest.satellite_id,
            "battery": latest.battery,
            "temperature": latest.temperature,
            "signal_strength": latest.signal_strength,
            "status": latest.status
        },
        "alerts": latest.alerts.split(",") if latest.alerts else []
    }


@app.get("/telemetry/history")
def get_history():
    db = SessionLocal()

    records = db.query(TelemetryRecord).order_by(TelemetryRecord.id.desc()).limit(20).all()

    db.close()

    return [
        {
            "timestamp": record.timestamp,
            "data": {
                "satellite_id": record.satellite_id,
                "battery": record.battery,
                "temperature": record.temperature,
                "signal_strength": record.signal_strength,
                "status": record.status
            },
            "alerts": record.alerts.split(",") if record.alerts else []
        }
        for record in records
    ]