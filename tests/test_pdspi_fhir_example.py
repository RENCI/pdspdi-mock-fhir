import requests
import time
from tx.fhir.utils import bundle, unbundle
import sys
import json
import os.path
# from tx.test.utils import bag_equal

patient_id = "1000"
patient_id2 = "2000"
patient_id3 = "0000" # non-existent
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

medication_request_resc = {
    "resourceType": "MedicationRequest",
    "subject": {
        "reference": f"Patient/{patient_id}"
    }
}


medication_request_resc2 = {
    "resourceType": "MedicationRequest",
    "subject": {
        "reference": f"Patient/{patient_id2}"
    }
}

php = "http://pdspi-fhir-example:8080"

def test_post_patient():

    try:
        resp1 = requests.post(f"{php}/Patient", json=patient_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Patient/{patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == patient_resc

    finally:
        requests.delete(f"{php}/resource")


def test_post_patient2():

    try:
        resp1 = requests.post(f"{php}/Patient", json=patient_resc)
    
        assert resp1.status_code == 200

        resp1 = requests.post(f"{php}/Patient", json=patient_resc2)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Patient/{patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == patient_resc

    finally:
        requests.delete(f"{php}/resource")


def test_post_patient_404():

    try:
        resp1 = requests.post(f"{php}/Patient", json=patient_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Patient/{patient_id3}")

        assert resp2.status_code == 404

    finally:
        requests.delete(f"{php}/resource")


def test_post_observation():

    try:
        resp1 = requests.post(f"{php}/Observation", json=observation_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Observation?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([observation_resc])

    finally:
        requests.delete(f"{php}/resource")


def test_post_condition():

    try:
        resp1 = requests.post(f"{php}/Condition", json=condition_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Condition?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([condition_resc])

    finally:
        requests.delete(f"{php}/resource")


def test_post_observation2():

    try:
        resp1 = requests.post(f"{php}/Observation", json=observation_resc)

        assert resp1.status_code == 200

        resp1 = requests.post(f"{php}/Observation", json=observation_resc2)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Observation?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([observation_resc])

    finally:
        requests.delete(f"{php}/resource")


def test_post_condition2():

    try:
        resp1 = requests.post(f"{php}/Condition", json=condition_resc)
    
        assert resp1.status_code == 200

        resp1 = requests.post(f"{php}/Condition", json=condition_resc2)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Condition?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([condition_resc])

    finally:
        requests.delete(f"{php}/resource")


def test_post_bundle_patient():

    try:
        resp1 = requests.post(f"{php}/Bundle", json=bundle([patient_resc, patient_resc2]))
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Patient/{patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == patient_resc

    finally:
        requests.delete(f"{php}/resource")


def test_post_bundle_observation():

    try:
        resp1 = requests.post(f"{php}/Bundle", json=bundle([observation_resc, observation_resc2]))
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Observation?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([observation_resc])

    finally:
        requests.delete(f"{php}/resource")


def test_post_bundle_condition():

    try:
        resp1 = requests.post(f"{php}/Bundle", json=bundle([condition_resc, condition_resc2]))
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/Condition?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([condition_resc])

    finally:
        requests.delete(f"{php}/resource")

def test_post_bundle_medication_request():

    try:
        resp1 = requests.post(f"{php}/Bundle", json=bundle([medication_request_resc, medication_request_resc2]))
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"{php}/MedicationRequest?patient={patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == bundle([medication_request_resc])

    finally:
        requests.delete(f"{php}/resource")

config = {
    "title": "FHIR data provider",
    "pluginType": "f",
    "pluginTypeTitle": "FHIR",
    "settingsDefaults": {
        "pluginSelectors": []
    }
}

def test_post_resources():

    try:
        resp1 = requests.post(f"{php}/Patient", json=patient_resc)
        resp1 = requests.post(f"{php}/Patient", json=patient_resc2)
        resp1 = requests.post(f"{php}/Observation", json=observation_resc)
        resp1 = requests.post(f"{php}/Observation", json=observation_resc2)
        resp1 = requests.post(f"{php}/Condition", json=condition_resc)
        resp1 = requests.post(f"{php}/Condition", json=condition_resc2)
        resp1 = requests.post(f"{php}/MedicationRequest", json=medication_request_resc)
        resp1 = requests.post(f"{php}/MedicationRequest", json=medication_request_resc2)
        
        resp1 = requests.post(f"{php}/resource", json={
            "resourceTypes": ["Patient", "Observation", "Condition", "MedicationRequest"],
            "patientIds": [patient_id, patient_id2]
        })
    
        assert resp1.status_code == 200
        patients = resp1.json()
        assert len(patients) == 2
        for patient in patients:
            assert patient["resourceType"] == "Bundle"
            assert patient["type"] == "batch-response"
            assert set(map(lambda x: x["resourceType"], unbundle(patient).value)) == {"Patient", "Bundle"}

    finally:
        requests.delete(f"{php}/resource")


def test_post_resources_output_to_file():

    try:
        resp1 = requests.post(f"{php}/Patient", json=patient_resc)
        resp1 = requests.post(f"{php}/Patient", json=patient_resc2)
        resp1 = requests.post(f"{php}/Observation", json=observation_resc)
        resp1 = requests.post(f"{php}/Observation", json=observation_resc2)
        resp1 = requests.post(f"{php}/Condition", json=condition_resc)
        resp1 = requests.post(f"{php}/Condition", json=condition_resc2)
        resp1 = requests.post(f"{php}/MedicationRequest", json=medication_request_resc)
        resp1 = requests.post(f"{php}/MedicationRequest", json=medication_request_resc2)

        files = [patient_id, patient_id2]
        resp = requests.post(f"{php}/resource", json={
            "resourceTypes": ["Patient", "Observation", "Condition", "MedicationRequest"],
            "patientIds": files,
            "outputFile": "outputname"
        })
    
        assert resp.status_code == 200


        assert "$ref" in resp.json()
        name = resp.json()["$ref"]
        patients = []
        for f in files:
            with open(os.path.join(os.environ.get("OUTPUT_DIR"), name, f + ".json")) as out:
                patients.append(json.load(out))
        assert len(patients) == 2
        for patient in patients:
            assert patient["resourceType"] == "Bundle"
            assert patient["type"] == "batch-response"
            assert set(map(lambda x: x["resourceType"], unbundle(patient).value)) == {"Patient", "Bundle"}

    finally:
        requests.delete(f"{php}/resource")


def test_config():
    resp = requests.get(f"{php}/config")
    
    assert resp.status_code == 200
    assert resp.json() == config
    
    
def test_ui():

    resp = requests.get(f"{php}/ui")
    
    assert resp.status_code == 200
    
# def test_get_patient_ids():

#     try:
#         resp1 = requests.post(f"{php}/Bundle", json=bundle([patient_resc, patient_resc2]))
    
#         assert resp1.status_code == 200

#         resp2 = requests.get(f"{php}/Patient")

#         assert resp2.status_code == 200
#         assert bag_equal(resp2.json(), [patient_resc["id"], patient_resc2["id"]])

#     finally:
#         requests.delete(f"{php}/resource")


