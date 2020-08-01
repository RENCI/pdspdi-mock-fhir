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
PATIENT_COLL = "Patient"
OBSERVATION_COLL = "Observation"
CONDITION_COLL = "Condition"
MEDICATION_REQUEST_COLL = "MedicationRequest"
resource_colls = [OBSERVATION_COLL, CONDITION_COLL, MEDICATION_REQUEST_COLL]

mongo_client = MongoClient(mongodb_host, mongodb_port, username=mongo_username, password=mongo_password, authSource=mongo_database)

mongo_client[mongo_database][PATIENT_COLL].create_index([("id", 1)])

for coll in resource_colls:
    mongo_client[mongo_database][coll].create_index([("subject.reference", 1)])

# todo implement transation
def update_patient(resource):
    try:
        patient_id = resource["id"]
    except:
        logger.error(f"cannot find id in resource {resource}")
        return
    coll = mongo_client[mongo_database][PATIENT_COLL]
    res = coll.replace_one({"id": patient_id}, copy.deepcopy(resource), upsert=True)


def update_resource(resc_type, patient_id, bundle):
    coll = mongo_client[mongo_database][resc_type]
    res = coll.delete_many({"subject.reference": f"Patient/{patient_id}"})
    logger.debug(f"bundle={bundle}, copy.deepcopy(bundle)={copy.deepcopy(bundle)}")
    records = unbundle(copy.deepcopy(bundle)).value
    if len(records) > 0:
        coll.insert_many(records)
        

def get_patient(patient_id):
    coll = mongo_client[mongo_database][PATIENT_COLL]
    res = coll.find({"id": patient_id})
    records = list(res)
    if len(records) == 0:
        return None
    elif len(records) > 1:
        raise RuntimeError(f"more than one patient with id {patient_id} {records}")

    resc = records[0]
    del resc["_id"]
    return resc


def get_resource(resource_type, patient_id):
    coll = mongo_client[mongo_database][resource_type]
    res = coll.find({"subject.reference": f"Patient/{patient_id}"})
    records = list(res)

    for resc in records:
        del resc["_id"]
    return bundle(records)

                    
def post_resource(resource):
    resc_type = resource["resourceType"]
    coll = mongo_client[mongo_database][resc_type]
    res = coll.insert_one(resource)
    logger.debug(f"cache.post_resource: post resource {resource}")


def post_resources(coll, resources):
    coll = mongo_client[mongo_database][coll]
    res = coll.insert_many(resources)


def post_bundle(bundle):
    rescs = unbundle(bundle).value
    x = {}
    for resc in rescs:
        resc_type = resc["resourceType"]
        if resc_type in x:
            x[resc_type].append(resc)
        else:
            x[resc_type] = [resc]
    for coll, rescs in x.items():
        post_resources(coll, rescs)


def delete_resource():
    db = mongo_client[mongo_database]
    db[PATIENT_COLL].remove()
    for resource_coll in resource_colls:
        db[resource_coll].remove()

