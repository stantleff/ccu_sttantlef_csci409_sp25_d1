from fastapi import FastAPI, Depends
import os
import httpx

API_KEY = os.getenv("MBTA_API_KEY", "")
ENDPOINT_URL = "https://api-v3.mbta.com"  # DO NOT CHANGE

app = FastAPI()

# Dependency to fetch all alerts
async def get_all_alerts(route: str = None, stop: str = None):
    params = {"api_key": API_KEY}

    if route:
        params["filter[route]"] = route
    if stop:
        params["filter[stop]"] = stop

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/alerts", params=params)
        response.raise_for_status()
        return response.json()

# Dependency to fetch a specific alert by ID
async def get_alert_by_id(alert_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/alerts/{alert_id}?api_key={API_KEY}")
        response.raise_for_status()
        return response.json()

# List alerts (supports query params)
@app.get("/")
async def read_alerts(route: str = None, stop: str = None, alerts=Depends(get_all_alerts)):
    return alerts

# Get one alert by ID
@app.get("/{alert_id}")
async def read_alert(alert_id: str, alert=Depends(get_alert_by_id)):
    return alert
