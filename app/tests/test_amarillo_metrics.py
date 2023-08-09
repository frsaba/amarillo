from datetime import datetime
import time
from urllib.request import HTTPBasicAuthHandler
import pytest
import re
import requests

from app.routers.metrics import *

def test_prometheus_requests_count():
    #first call after startup
    response =requests.get("http://127.0.0.1:8000/amarillo-metrics/", auth=HTTPBasicAuthHandler("user1", "pw1"))
    assert response.status_code == 200

    response_text = response.text

    regex_pattern = r'http_requests_total{handler="/amarillo-metrics/",method="GET",status="2xx"} [0-9]{1,}\.0'
    assert re.search(regex_pattern, response_text) is None # at the first request there won't be a line with this, just in the sencond call

    #second call after first run
    response =requests.get("http://127.0.0.1:8000/amarillo-metrics/", auth=HTTPBasicAuthHandler("user1", "pw1"))
    assert response.status_code == 200

    response_text = response.text

    regex_pattern = r'http_requests_total{handler="/amarillo-metrics/",method="GET",status="2xx"} [0-9]{1,}\.0'
    assert re.search(regex_pattern, response_text) is not None

def test_custom_prometheus_field():

    response =requests.get("http://127.0.0.1:8000/amarillo-metrics/", auth=HTTPBasicAuthHandler("user1", "pw1"))
    assert response.status_code == 200

    response_text = response.text

    regex_pattern = r'amarillo_trips_number [0-9]{1,}\.0'
    assert re.search(regex_pattern, response_text) is not None