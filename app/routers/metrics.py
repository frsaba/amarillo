import logging
import os.path
import random

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime



from prometheus_client.exposition import generate_latest
from prometheus_client import Gauge
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)

security = HTTPBasic()


trips_number = Gauge("amarillo_trips_number", "Number of trips.")

# CONSTANT_LABEL = "amarillo_trips_number" 


router = APIRouter(
    prefix="/amarillo-metrics",
    tags=["amarillo_metrics"]
)


fake_users_db = {
    "user1": {
        "username": "user1",
        "password": "pw1",  # need hash or any auth service
    }
}



@router.get("/")
def metrics(credentials: HTTPBasicCredentials = Depends(security)):
    user = fake_users_db.get(credentials.username)
    if user is None or not credentials.password == user["password"]:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    trips_number.set(random.randint(0,100))
    return PlainTextResponse(content=generate_latest())

