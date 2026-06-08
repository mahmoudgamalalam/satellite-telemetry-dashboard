import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.main import Telemetry, check_alerts
def test_low_battery_alert():
    data = Telemetry(
        satellite_id="SAT-001",
        battery=10,
        temperature=25,
        signal_strength=-70,
        status="OK"
    )

    alerts = check_alerts(data)

    assert "LOW BATTERY" in alerts


def test_high_temperature_alert():
    data = Telemetry(
        satellite_id="SAT-001",
        battery=80,
        temperature=45,
        signal_strength=-70,
        status="OK"
    )

    alerts = check_alerts(data)

    assert "HIGH TEMPERATURE" in alerts


def test_weak_signal_alert():
    data = Telemetry(
        satellite_id="SAT-001",
        battery=80,
        temperature=25,
        signal_strength=-95,
        status="OK"
    )

    alerts = check_alerts(data)

    assert "WEAK SIGNAL" in alerts


def test_no_alerts():
    data = Telemetry(
        satellite_id="SAT-001",
        battery=80,
        temperature=25,
        signal_strength=-70,
        status="OK"
    )

    alerts = check_alerts(data)

    assert alerts == []