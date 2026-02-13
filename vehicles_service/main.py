from fastapi import FastAPI, Depends
import os
import httpx

API_KEY = os.getenv("MBTA_API_KEY", "")
ENDPOINT_URL = "https://api-v3.mbta.com"

app = FastAPI()

# Dependency to fetch all vehicles
async def get_all_vehicles(route: str = None, revenue: bool = None):
    params = {"api_key": API_KEY}

    if route:
        params["filter[route]"] = route

    if revenue is not None:
        params["filter[revenue]"] = str(revenue).lower()

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/vehicles", params=params)
        response.raise_for_status()
        return response.json()

# Dependency to fetch a specific vehicle by ID
async def get_vehicle_by_id(vehicle_id: str):
    params = {"api_key": API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/vehicles/{vehicle_id}", params=params)
        response.raise_for_status()
        return response.json()

@app.get("/")
async def read_vehicles(route: str = None, revenue: bool = None, vehicles=Depends(get_all_vehicles)):
    return vehicles

@app.get("/{vehicle_id}")
async def read_vehicle(vehicle_id: str, vehicle=Depends(get_vehicle_by_id)):
    return vehicle
