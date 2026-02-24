import base64
import os
import secrets

from fastapi import FastAPI
from starlette.responses import Response

from routes_service.main import app as routes_app
from lines_service.main import app as lines_app
from alerts_service.main import app as alerts_app
from vehicles_service.main import app as vehicles_app

app = FastAPI(title="API Gateway")

@app.middleware("http")
async def basic_auth_middleware(request, call_next):
    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.lower().startswith("basic "):
        return Response(
            content="Authentication required",
            status_code=401,
            headers={"WWW-Authenticate": "Basic"},
        )

    try:
        encoded = auth_header.split(" ", 1)[1].strip()
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
    except Exception:
        return Response(
            content="Invalid authentication header",
            status_code=401,
            headers={"WWW-Authenticate": "Basic"},
        )

    expected_username = os.getenv("BASIC_AUTH_USERNAME", "admin")
    expected_password = os.getenv("BASIC_AUTH_PASSWORD", "password")

    if not (
        secrets.compare_digest(username, expected_username)
        and secrets.compare_digest(password, expected_password)
    ):
        return Response(
            content="Invalid authentication credentials",
            status_code=401,
            headers={"WWW-Authenticate": "Basic"},
        )

    return await call_next(request)

# Mount microservices
app.mount("/routes", routes_app)
app.mount("/lines", lines_app)
app.mount("/alerts", alerts_app)
app.mount("/vehicles", vehicles_app)
