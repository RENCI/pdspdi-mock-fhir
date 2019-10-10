from pdsdpimockfhir import dispatcher

def get_patient(patient_id):
    return dispatcher.get_patient(patient_id)

def get_observation(patient_id):
    return dispatcher.get_observation(patient_id)

def get_condition(patient_id):
    return dispatcher.get_condition(patient_id)

def post_bundle(body):
    return dispatcher.post_bundle(body)

def post_patient(body):
    return dispatcher.post_patient(body)

def post_observation(body):
    return dispatcher.post_observation(body)

def post_condition(body):
    return dispatcher.post_condition(body)

def delete_resource():
    return dispatcher.delete_resource(body)



