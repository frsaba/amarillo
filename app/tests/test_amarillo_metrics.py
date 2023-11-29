from datetime import datetime
import time
import pytest
import re
import requests

from app.routers.metrics import *
from app.services.secrets import secrets

API_URL = "http://127.0.0.1:8000"
auth = (secrets.metrics_user, secrets.metrics_password)

def test_prometheus_requests_count_first():
    #first call after startup
    response =requests.get(f"{API_URL}/metrics/", auth=auth)
    assert response.status_code == 200, "Invalid status code"

    response_text = response.text

    regex_pattern = r'http_requests_total{handler="/metrics/",method="GET",status="2xx"}'

    assert re.search(regex_pattern, response_text) is None, "This is not a fresh run of the site"

def test_prometheus_requests_count_second():
    #second call after first run
    response =requests.get(f"{API_URL}/metrics/", auth=auth)
    assert response.status_code == 200, "Invalid status code"

    response_text = response.text

    regex_pattern = r'http_requests_total{handler="/metrics/",method="GET",status="2xx"} 2.0'
    assert re.search(regex_pattern, response_text) is not None, "There is no total request counter or not the 2nd call for /amarillo-metrics"

def test_prometheus_region_counter_first():
    #check if there is no request for region (should be 0)
    response = requests.get(f"{API_URL}/metrics/", auth=auth)
    assert response.status_code == 200, "Invalid status code"

    response_text = response.text
    regex_pattern = r'http_requests_total{handler="/region/",method="GET",status="2xx"}'
    assert re.search(regex_pattern, response_text) is None, "The total request counter value is not 0 for /region"

def test_prometheus_region_counter_second():
    #call region endpoint, checks if it is the first request
    _ = requests.get(f"{API_URL}/region/")
    response =requests.get(f"{API_URL}/metrics/", auth=auth)
    assert response.status_code == 200, "Invalid status code"

    response_text = response.text
    regex_pattern = r'http_requests_total{handler="/region/",method="GET",status="2xx"} 2.0'
    assert re.search(regex_pattern, response_text) is not None, "There is no total request counter or not the 1st call for /region"


def test_amarillo_trips_number_total():

    response =requests.get(f"{API_URL}/metrics/", auth=auth)
    assert response.status_code == 200, "Invalid status code"

    response_text = response.text

    regex_pattern = r'amarillo_trips_number_total [0-9]{1,}\.0'
    assert re.search(regex_pattern, response_text) is not None, "There is no custom metric named 'amarillo_trips_number_total'"