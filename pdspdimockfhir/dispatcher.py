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


mongo_client = MongoClient(mongodb_host, mongodb_port, username=mongo_username, password=mongo_password, authSource=mongo_database)

def get_patient(patient_id):
    coll = mongo_client[mongo_database]["Patient"]
    res = coll.find({"id": patient_id})
    records = list(res)
    if len(records) != 1:
        raise RuntimeError("zero or more than one patient")

    return records[0]

def get_observation(patient_id):
    coll = mongo_client[mongo_database]["Observation"]
    res = coll.find({"subject.reference": f"Patient/{patient_id}")
    records = list(res)

    return records

def get_condition(patient_id):
    coll = mongo_client[mongo_database]["Condition"]
    res = coll.find({"subject.reference": f"Patient/{patient_id}")
    records = list(res)

    return records

