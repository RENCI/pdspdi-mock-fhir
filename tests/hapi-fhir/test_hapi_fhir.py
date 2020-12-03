import requests
import time
import os
from pdsdpimockfhir.utils import bundle

patient_id = os.environ["PATIENT_ID_EXISTENT"]
patient_id2 = os.environ["PATIENT_ID_NONEXISTENT"]

def test_get_patient():

    try:
        resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id}")

        assert resp2.status_code == 200
        print(resp2.content)
        assert resp2.json()["id"] == patient_id

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_get_patient2():

    try:
        resp = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id}")

        assert resp.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id}")

        assert resp2.status_code == 200

        assert resp.json() == resp2.json()

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_get_patient_nonexistent():

    try:
        resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id2}")

        assert resp2.status_code == 404

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_get_observation():

    try:
        resp2 = requests.get(f"http://pds-mock-fhir:8080/Observation?patient={patient_id}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_get_observation_nonexistent():

    try:
        resp2 = requests.get(f"http://pds-mock-fhir:8080/Observation?patient={patient_id2}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_get_condition():

    try:
        resp2 = requests.get(f"http://pds-mock-fhir:8080/Condition?patient={patient_id}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_get_condition_nonexistent():

    try:
        resp2 = requests.get(f"http://pds-mock-fhir:8080/Condition?patient={patient_id2}")

        assert resp2.status_code == 200

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


