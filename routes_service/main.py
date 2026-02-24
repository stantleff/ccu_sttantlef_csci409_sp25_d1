from fastapi import FastAPI, Depends, HTTPException
import os
import requests

from auth import verify_basic_auth

API_KEY = os.getenv("MBTA_API_KEY", "").strip()
ENDPOINT_URL = "https://api-v3.mbta.com"

app = FastAPI(title="Routes Service", dependencies=[Depends(verify_basic_auth)])


def mbta_get(path: str):
    """
    Helper to call MBTA and safely handle bad responses
    """
    url = f"{ENDPOINT_URL}{path}"




    headers = {}
    if API_KEY:
        headers["x-api-key"] = API_KEY

    response = requests.get(url, headers=headers)

    # If MBTA returned an error HTTP status, show it clearly
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "MBTA API returned an error status",
                "status_code": response.status_code,
                "url": url,
                "body": response.text,
            },
        )

    # MBTA should return JSON. If it doesn't, handle it.
    try:
        payload = response.json()
    except Exception:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "MBTA API did not return valid JSON",
                "url": url,
                "body": response.text,
            },
        )

    # MBTA normal responses contain "data".
    if "data" not in payload:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "MBTA response missing expected 'data' key",
                "url": url,
                "payload": payload,
            },
        )

    return payload["data"]


# List all routes
@app.get("/")
def get_routes():
    routes_list = []
    routes = mbta_get("/routes")

    for route in routes:
        attrs = route.get("attributes", {}) or {}
        routes_list.append(
            {
                "id": route.get("id"),
                "type": route.get("type"),
                "color": attrs.get("color"),
                "text_color": attrs.get("text_color"),
                "description": attrs.get("description"),
                "long_name": attrs.get("long_name"),
                "route_type": attrs.get("type"),
            }
        )

    return {"routes": routes_list}


# Get one route by id
@app.get("/{route_id}")
def get_route(route_id: str):
    route_data = mbta_get(f"/routes/{route_id}")

    attrs = route_data.get("attributes", {}) or {}

    route = {
        "id": route_data.get("id"),
        "type": route_data.get("type"),
        "color": attrs.get("color"),
        "text_color": attrs.get("text_color"),
        "description": attrs.get("description"),
        "long_name": attrs.get("long_name"),
        "route_type": attrs.get("type"),
    }

    return {"route": route}

