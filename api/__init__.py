from pdsdpimockfhir import dispatcher
import sys

def get_patient(patient_id):
    return dispatcher.get_patient(patient_id)

def get_observation(patient):
    return dispatcher.get_resource("Observation", patient)

def get_condition(patient):
    return dispatcher.get_resource("Condition", patient)

def get_medication_request(patient):
    return dispatcher.get_resource("MedicationRequest", patient)

def post_bundle(body):
    return dispatcher.post_bundle(body)

def post_patient(body):
    print(f"posting patient {body}")
    sys.stdout.flush()
    return dispatcher.post_patient(body)

def post_observation(body):
    print(f"posting observation {body}")
    sys.stdout.flush()   
    return dispatcher.post_resource(body)

def post_condition(body):
    return dispatcher.post_resource(body)

def post_medication_request(body):
    return dispatcher.post_resource(body)

def delete_resource():
    return dispatcher.delete_resource()

def delete_patient():
    return dispatcher.delete_patient()

def delete_observation():
    return dispatcher.delete_observation()

def delete_condition():
    return dispatcher.delete_condition()

def post_resources(body):
    return dispatcher.post_resources(body["resourceTypes"], body["pids"])

config = {
    "title": "FHIR data provider",
    "pluginType": "f",
    "pluginTypeTitle": "FHIR",
    "settingsDefaults": {
        "pluginSelectors": []
    }
}

def get_config():
    return config
