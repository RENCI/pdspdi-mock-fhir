import os
import copy
from pymongo import MongoClient
from flask import Response
from bson.json_util import dumps
import logging
import time
import sys
from .utils import bundle, unbundle
import copy


mongodb_host = os.environ["MONGO_HOST"]
mongodb_port = int(os.environ["MONGO_PORT"])
mongo_database = os.environ["MONGO_DATABASE"]
mongo_username = os.environ["MONGO_NON_ROOT_USERNAME"]
mongo_password = os.environ["MONGO_NON_ROOT_PASSWORD"]
cache_ttl = float(os.environ.get("CACHE_TTL", "inf"))
PATIENT_COLL = "Patient"
OBSERVATION_COLL = "Observation"
CONDITION_COLL = "Condition"
RETRIEVE_TIME_COLL = "RetrieveTime"
COLL_DICT = {
    "Observation": OBSERVATION_COLL,
    "Condition": CONDITION_COLL
}

mongo_client = MongoClient(mongodb_host, mongodb_port, username=mongo_username, password=mongo_password, authSource=mongo_database)

# todo implement transation
def update_patient(resource, retrieve_time):
    try:
        patient_id = resource["id"]
    except:
        print(f"cannot find id in resource {reosurce}")
        sys.stdout.flush()
        return
    coll = mongo_client[mongo_database][PATIENT_COLL]
    res = coll.replace_one({"id": patient_id}, copy.deepcopy(resource), upsert=True)
    update_retrieve_time("Patient", patient_id, retrieve_time)


def update_resource(resc_type, patient_id, bundle, retrieve_time):
    coll = mongo_client[mongo_database][COLL_DICT[resc_type]]
    res = coll.delete_many({"subject.reference": f"Patient/{patient_id}"})
    print(f"bundle={bundle}, copy.deepcopy(bundle)={copy.deepcopy(bundle)}")
    sys.stdout.flush()
    records = unbundle(copy.deepcopy(bundle))
    if len(records) > 0:
        coll.insert_many(records)
    update_retrieve_time(resc_type, patient_id, retrieve_time)
        

def update_retrieve_time(resource_type, patient_id, curr_time):
    rt_coll = mongo_client[mongo_database][RETRIEVE_TIME_COLL]
    print(f"inserting retrieve time for {resource_type} {patient_id} as {curr_time}")
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
    print(f"retrieve_time of {patient_id} is {rt}")
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
    coll = mongo_client[mongo_database][COLL_DICT[resource_type]]
    res = coll.find({"subject.reference": f"Patient/{patient_id}"})
    records = list(res)

    for resc in records:
        del resc["_id"]
    return bundle(records)

                    
def post_resource(resource, retrieve_time):
    resc_type = resource["resourceType"]
    coll = mongo_client[mongo_database][COLL_DICT[resc_type]]
    res = coll.insert_one(resource)
    print(f"cache.post_resource: post resource {resource}")
    sys.stdout.flush()
    update_retrieve_time(resc_type, resource["subject"]["reference"][8:], retrieve_time)  


def post_bundle(bundle, retrieve_time):
    for resc in unbundle(bundle):
        post_resource(resc, retrieve_time)


def delete_resource():
    db = mongo_client[mongo_database]
    db[PATIENT_COLL].remove()
    db[CONDITION_COLL].remove()
    db[OBSERVATION_COLL].remove()
    db[RETRIEVE_TIME_COLL].remove()

