import os
import copy
from pymongo import MongoClient
from flask import Response
from bson.json_util import dumps
import logging


mongodb_host = os.environ["MONGO_HOST"]
mongodb_port = int(os.environ["MONGO_PORT"])
mongo_database = os.environ["MONGO_DATABASE"]
mongo_username = os.environ["MONGO_NON_ROOT_USERNAME"]
mongo_password = os.environ["MONGO_NON_ROOT_PASSWORD"]
PATIENT_COLL = "Patient"
OBSERVATION_COLL = "Observation"
CONDITION_COLL = "Condition"

mongo_client = MongoClient(mongodb_host, mongodb_port, username=mongo_username, password=mongo_password, authSource=mongo_database)


def get_patient(patient_id):
    coll = mongo_client[mongo_database][PATIENT_COLL]
    res = coll.find({"id": patient_id})
    records = list(res)
    if len(records) == 0:
        return "not found", 404
    elif len(records) > 1:
        raise RuntimeError(f"more than one patient with id {patient_id} {records}")

    resc = records[0]
    del resc["_id"]
    return resc


def get_observation(patient_id):
    coll = mongo_client[mongo_database][OBSERVATION_COLL]
    res = coll.find({"subject.reference": f"Patient/{patient_id}"})
    records = list(res)

    for resc in records:
        del resc["_id"]
    return records

                    
def get_condition(patient_id):
    coll = mongo_client[mongo_database][CONDITION_COLL]
    res = coll.find({"subject.reference": f"Patient/{patient_id}"})
    records = list(res)

    for resc in records:
        del resc["_id"]
    return records


def post_patient(resource):
    coll = mongo_client[mongo_database][PATIENT_COLL]
    res = coll.insert_one(resource)
    res = coll.find()
    records = list(res)

    return "record inserted"


def post_observation(resource):
    coll = mongo_client[mongo_database][OBSERVATION_COLL]
    res = coll.insert_one(resource)
    return "record inserted"


def post_condition(resource):
    coll = mongo_client[mongo_database][CONDITION_COLL]
    res = coll.insert_one(resource)
    return "record inserted"


def post_bundle(bundle):
    db = mongo_client[mongo_database]
    for entry in bundle["entry"]:
        resc = entry["resource"]
        coll = db[resc["resourceType"]]
        coll.insert_one(resc)


def delete_resource():
    db = mongo_client[mongo_database]
    db[PATIENT_COLL].remove()
    db[CONDITION_COLL].remove()
    db[OBSERVATION_COLL].remove()


def delete_patient():
    db = mongo_client[mongo_database]
    db[PATIENT_COLL].remove()


def delete_observation():
    db = mongo_client[mongo_database]
    db[OBSERVATION_COLL].remove()


def delete_condition():
    db = mongo_client[mongo_database]
    db[CONDITION_COLL].remove()


