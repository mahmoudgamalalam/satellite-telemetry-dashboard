from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

telemetry_store = []


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
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "data": data.dict(),
        "alerts": check_alerts(data)
    }

    telemetry_store.append(record)

    return {
        "message": "Telemetry received",
        "alerts": record["alerts"]
    }


@app.get("/telemetry/latest")
def get_latest_telemetry():
    if not telemetry_store:
        return {"message": "No telemetry received yet"}

    return telemetry_store[-1]


@app.get("/telemetry/history")
def get_history():
    return telemetry_store