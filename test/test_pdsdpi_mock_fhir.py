import requests
import time
from pdsdpimockfhir.utils import bundle
# from tx.test.utils import bag_equal

patient_id = "1000"
patient_id2 = "2000"
patient_resc = {
    "id": patient_id,
    "resourceType": "Patient"
}

patient_resc2 = {
    "id": patient_id2,
    "resourceType": "Patient"
}

observation_resc = {
    "resourceType": "Observation",
    "subject": {
        "reference": f"Patient/{patient_id}"
    }
}


condition_resc = {
    "resourceType": "Condition",
    "subject": {
        "reference": f"Patient/{patient_id}"
    }
}

observation_resc2 = {
    "resourceType": "Observation",
    "subject": {
        "reference": f"Patient/{patient_id2}"
    }
}


condition_resc2 = {
    "resourceType": "Condition",
    "subject": {
        "reference": f"Patient/{patient_id2}"
    }
}


def test_post_patient():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Patient", json=patient_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == patient_resc

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_patient2():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Patient", json=patient_resc)
    
        assert resp1.status_code == 200

        resp1 = requests.post("http://pds-mock-fhir:8080/Patient", json=patient_resc2)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == patient_resc

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_patient_404():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Patient", json=patient_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id2}")

        assert resp2.status_code == 404

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_observation():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Observation", json=observation_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Observation?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([observation_resc])

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_condition():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Condition", json=condition_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Condition?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([condition_resc])

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_observation2():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Observation", json=observation_resc)

        assert resp1.status_code == 200

        resp1 = requests.post("http://pds-mock-fhir:8080/Observation", json=observation_resc2)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Observation?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([observation_resc])

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_condition2():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Condition", json=condition_resc)
    
        assert resp1.status_code == 200

        resp1 = requests.post("http://pds-mock-fhir:8080/Condition", json=condition_resc2)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Condition?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([condition_resc])

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_bundle_patient():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Bundle", json=bundle([patient_resc, patient_resc2]))
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient/{patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == patient_resc

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_bundle_observation():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Bundle", json=bundle([observation_resc, observation_resc2]))
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Observation?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([observation_resc])

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")


def test_post_bundle_condition():

    try:
        resp1 = requests.post("http://pds-mock-fhir:8080/Bundle", json=bundle([condition_resc, condition_resc2]))
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pds-mock-fhir:8080/Condition?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([condition_resc])

    finally:
        requests.delete("http://pds-mock-fhir:8080/resource")

def test_ui():
    resp = requests.get("http://pds-mock-fhir:8080/ui")
    
    assert resp.status_code == 200
    
# def test_get_patient_ids():

#     try:
#         resp1 = requests.post("http://pds-mock-fhir:8080/Bundle", json=bundle([patient_resc, patient_resc2]))
    
#         assert resp1.status_code == 200

#         resp2 = requests.get(f"http://pds-mock-fhir:8080/Patient")

#         assert resp2.status_code == 200
#         assert bag_equal(resp2.json(), [patient_resc["id"], patient_resc2["id"]])

#     finally:
#         requests.delete("http://pds-mock-fhir:8080/resource")


