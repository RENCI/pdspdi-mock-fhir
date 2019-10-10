import requests
import time
import ndjson

patient_id = "1000"
patient_resc = {
    "id": patient_id,
    "resourceType": "Patient"
}

def test_post_patient():

    try:
        resp1 = requests.post("http://pdsdpi-mock-fhir:8080/Patient", json=patient_resc)
    
        assert resp1.status_code == 200

        resp2 = requests.get(f"http://pdsdpi-mock-fhir:8080/Patient/{patient_id}")

        assert resp2.status_code == 200
        assert resp2.json() == patient_resc

    finally:
        requests.delete("http://pdsdpi-mock-fhir:8080/resource")
