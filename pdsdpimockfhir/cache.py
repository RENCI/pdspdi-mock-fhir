import os
import copy
from pymongo import MongoClient
from flask import Response
from bson.json_util import dumps
import logging
import time
import sys
from tx.fhir.utils import bundle, unbundle
import copy
from tx.logging.utils import getLogger


logger = getLogger(__name__, logging.INFO)


mongodb_host = os.environ["MONGO_HOST"]
mongodb_port = int(os.environ["MONGO_PORT"])
mongo_database = os.environ["MONGO_DATABASE"]
mongo_username = os.environ["MONGO_NON_ROOT_USERNAME"]
mongo_password = os.environ["MONGO_NON_ROOT_PASSWORD"]
cache_ttl = float(os.environ.get("CACHE_TTL", "inf"))
PATIENT_COLL = "Patient"
OBSERVATION_COLL = "Observation"
CONDITION_COLL = "Condition"
MEDICATION_REQUEST_COLL = "MedicationRequest"
RETRIEVE_TIME_COLL = "RetrieveTime"
resource_colls = [OBSERVATION_COLL, CONDITION_COLL, MEDICATION_REQUEST_COLL]

mongo_client = MongoClient(mongodb_host, mongodb_port, username=mongo_username, password=mongo_password, authSource=mongo_database)

# todo implement transation
def update_patient(resource, retrieve_time):
    try:
        patient_id = resource["id"]
    except:
        logger.error(f"cannot find id in resource {resource}")
        return
    coll = mongo_client[mongo_database][PATIENT_COLL]
    res = coll.replace_one({"id": patient_id}, copy.deepcopy(resource), upsert=True)
    update_retrieve_time("Patient", patient_id, retrieve_time)


def update_resource(resc_type, patient_id, bundle, retrieve_time):
    coll = mongo_client[mongo_database][resc_type]
    res = coll.delete_many({"subject.reference": f"Patient/{patient_id}"})
    logger.debug(f"bundle={bundle}, copy.deepcopy(bundle)={copy.deepcopy(bundle)}")
    records = unbundle(copy.deepcopy(bundle)).value
    if len(records) > 0:
        coll.insert_many(records)
    update_retrieve_time(resc_type, patient_id, retrieve_time)
        

def update_retrieve_time(resource_type, patient_id, curr_time):
    rt_coll = mongo_client[mongo_database][RETRIEVE_TIME_COLL]
    logger.debug(f"inserting retrieve time for {resource_type} {patient_id} as {curr_time}")
    rt_coll.replace_one({"patient_id": patient_id, "resourceType": resource_type}, {"patient_id": patient_id, "resourceType": resource_type, "retrieve_time": curr_time}, upsert=True)


def get_retrieve_time(resource_type, patient_id):
    rt_coll = mongo_client[mongo_database][RETRIEVE_TIME_COLL]
    rt = rt_coll.find_one({"patient_id": patient_id, "resourceType": resource_type})
    if rt is None:
        return None
    else:
        return rt["retrieve_time"]


def get_patient(patient_id):
    curr_time = time.time()
    rt = get_retrieve_time("Patient", patient_id)
    logger.debug(f"retrieve_time of {patient_id} is {rt}")
    if rt is None or curr_time - rt > cache_ttl:
        return None
    coll = mongo_client[mongo_database][PATIENT_COLL]
    res = coll.find({"id": patient_id})
    records = list(res)
    if len(records) == 0:
        raise RuntimeError(f"no patient with id {patient_id}")
    elif len(records) > 1:
        raise RuntimeError(f"more than one patient with id {patient_id} {records}")

    resc = records[0]
    del resc["_id"]
    return resc


def get_resource(resource_type, patient_id):
    curr_time = time.time()
    rt = get_retrieve_time(resource_type, patient_id)
    if rt is None or curr_time - rt > cache_ttl:
        return None
    coll = mongo_client[mongo_database][resource_type]
    res = coll.find({"subject.reference": f"Patient/{patient_id}"})
    records = list(res)

    for resc in records:
        del resc["_id"]
    return bundle(records)

                    
def post_resource(resource, retrieve_time):
    resc_type = resource["resourceType"]
    coll = mongo_client[mongo_database][resc_type]
    res = coll.insert_one(resource)
    logger.debug(f"cache.post_resource: post resource {resource}")
    if resc_type == "Patient":
        patient_id = resource["id"]
    else:
        patient_id = resource["subject"]["reference"][8:]
    update_retrieve_time(resc_type, patient_id, retrieve_time)  


def post_bundle(bundle, retrieve_time):
    for resc in unbundle(bundle).value:
        post_resource(resc, retrieve_time)


def delete_resource():
    db = mongo_client[mongo_database]
    db[PATIENT_COLL].remove()
    for resource_coll in resource_colls:
        db[resource_coll].remove()
    db[RETRIEVE_TIME_COLL].remove()

