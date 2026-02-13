from fastapi import FastAPI
import os
import requests

API_KEY = os.getenv("MBTA_API_KEY", "")
ENDPOINT_URL = "https://api-v3.mbta.com"  # DO NOT CHANGE

app = FastAPI()

# List all lines
@app.get("/")
def get_lines():
    lines_list = []
    response = requests.get(ENDPOINT_URL + f"/lines?api_key={API_KEY}")
    lines = response.json()["data"]

    for line in lines:
        attrs = line["attributes"]
        lines_list.append({
            "id": line["id"],
            "text_color": attrs["text_color"],
            "short_name": attrs["short_name"],
            "long_name": attrs["long_name"],
            "color": attrs["color"],
        })

    return {"lines": lines_list}

# Get one line by id
@app.get("/{line_id}")
def get_line(line_id: str):
    response = requests.get(ENDPOINT_URL + f"/lines/{line_id}?api_key={API_KEY}")
    line_data = response.json()["data"]
    attrs = line_data["attributes"]

    line = {
        "id": line_data["id"],
        "text_color": attrs["text_color"],
        "short_name": attrs["short_name"],
        "long_name": attrs["long_name"],
        "color": attrs["color"],
    }

    return {"lines": line}
