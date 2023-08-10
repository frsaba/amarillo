import json
import logging
import os.path
import random
from typing import Callable
from app.utils import container

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime



from prometheus_client.exposition import generate_latest
from prometheus_client import Gauge, Counter
from prometheus_fastapi_instrumentator.metrics import Info
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)

security = HTTPBasic()

total_requests_metric = Gauge(
    "total_requests",
    "Total requests for a specific endpoint",
    ["endpoint"]
)

def amarillo_trips_number_total() -> Callable[[Info], None]:
    METRIC = Gauge("amarillo_trips_number_total", "Total number of trips.")

    def instrumentation(info: Info) -> None:
       
        #TODO get total trips
        METRIC.set(100)

    return instrumentation



router = APIRouter(
    prefix="/metrics",
    tags=["amarillo_metrics"]
)


fake_users_db = {
    "user1": {
        "username": "user1",
        "password": "pw1",  #TODO need hash or any auth service
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
    
    total_requests_metric.labels(endpoint="/amarillo-metrics").inc()
    return PlainTextResponse(content=generate_latest())
