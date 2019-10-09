import pdsdatapluginmockfhir.dispatcher

def get_patient(patient_id):
    return pdsdatapluginmockfhir.dispatcher.get_patient(patient_id)

def get_observation(patient_id):
    return pdsdatapluginmockfhir.dispatcher.get_observation(patient_id)

def get_condition(patient_id):
    return pdsdatapluginmockfhir.dispatcher.get_condition(patient_id)




