import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/telemetry/latest"

st.set_page_config(
    page_title="Satellite Telemetry Dashboard",
    layout="wide"
)

st.title("Satellite Telemetry Monitoring Dashboard")
st.caption("Live simulated satellite health data")

placeholder = st.empty()

while True:
    response = requests.get(API_URL)
    data = response.json()

    with placeholder.container():
        if "message" in data:
            st.warning(data["message"])
        else:
            telemetry = data["data"]
            alerts = data["alerts"]

            st.subheader(f"Satellite: {telemetry['satellite_id']}")

            col1, col2, col3 = st.columns(3)

            col1.metric("Battery", f"{telemetry['battery']}%")
            col2.metric("Temperature", f"{telemetry['temperature']} °C")
            col3.metric("Signal Strength", f"{telemetry['signal_strength']} dBm")

            st.write("Status:", telemetry["status"])

            if alerts:
                st.error("Alerts: " + ", ".join(alerts))
            else:
                st.success("All systems nominal")

            st.caption(f"Last updated: {data['timestamp']}")

    time.sleep(3)
    st.rerun()