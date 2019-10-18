import requests
import time
from pdsdpimockfhir.utils import bundle

patient_id = 14
patient_id2 = 15

def test_get_patient():

    try:
        resp2 = requests.get(f"http://pdsdpi-mock-fhir:8080/Patient/{patient_id}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pdsdpi-mock-fhir:8080/resource")


def test_get_patient_nonexistent():

    try:
        resp2 = requests.get(f"http://pdsdpi-mock-fhir:8080/Patient/{patient_id2}")

        assert resp2.status_code == 404

    finally:
        requests.delete("http://pdsdpi-mock-fhir:8080/resource")


def test_get_observation():

    try:
        resp2 = requests.get(f"http://pdsdpi-mock-fhir:8080/Observation?patient={patient_id}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pdsdpi-mock-fhir:8080/resource")


def test_get_observation_nonexistent():

    try:
        resp2 = requests.get(f"http://pdsdpi-mock-fhir:8080/Observation?patient={patient_id2}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pdsdpi-mock-fhir:8080/resource")


def test_get_condition():

    try:
        resp2 = requests.get(f"http://pdsdpi-mock-fhir:8080/Condition?patient={patient_id}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pdsdpi-mock-fhir:8080/resource")


def test_get_condition_nonexistent():

    try:
        resp2 = requests.get(f"http://pdsdpi-mock-fhir:8080/Condition?patient={patient_id2}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pdsdpi-mock-fhir:8080/resource")


