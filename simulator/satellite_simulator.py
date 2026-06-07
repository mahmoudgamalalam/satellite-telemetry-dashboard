import requests
import random
import time

API_URL = "http://127.0.0.1:8001/telemetry"

while True:

    telemetry = {
        "satellite_id": "SAT-001",
        "battery": round(random.uniform(10, 100), 2),
        "temperature": round(random.uniform(10, 50), 2),
        "signal_strength": round(random.uniform(-100, -50), 2),
        "status": "OK"
    }

    response = requests.post(API_URL, json=telemetry)

    print("Sent:", telemetry)
    print("Response:", response.json())
    print("-" * 40)

    time.sleep(3)