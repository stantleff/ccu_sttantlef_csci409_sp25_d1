from fastapi import FastAPI

from routes_service.main import app as routes_app
from lines_service.main import app as lines_app
from alerts_service.main import app as alerts_app
from vehicles_service.main import app as vehicles_app

app = FastAPI()

# Mount each microservice under a context path
app.mount("/routes", routes_app)
app.mount("/lines", lines_app)
app.mount("/alerts", alerts_app)
app.mount("/vehicles", vehicles_app)
