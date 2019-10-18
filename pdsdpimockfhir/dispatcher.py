import os
import copy
from pymongo import MongoClient
from flask import Response
from bson.json_util import dumps
import logging
import time
import pdsdpimockfhir.cache as cache
import requests
import sys


fhir_server_url_base = os.environ.get("FHIR_SERVER_URL_BASE")


def get_patient(patient_id):
    resc = cache.get_patient(patient_id)

    if resc is not None:
        return resc
    elif fhir_server_url_base is not None:
        curr_time = time.time()
        resp = requests.get(f"{fhir_server_url_base}/Patient/{patient_id}")
        if resp.status_code == 404:
            return "not found", 404
        else:
            resc = resp.json()
            cache.update_patient(resc, curr_time)
            return resc
    else:
        return "not found", 404
        

def get_resource(resc_type, patient_id):
    bundle = cache.get_resource(resc_type, patient_id)

    if bundle is not None:
        return bundle
    elif fhir_server_url_base is not None:
        curr_time = time.time()
        resp = requests.get(f"{fhir_server_url_base}/{resc_type}?patient={patient_id}")
        print(f"{fhir_server_url_base}/{resc_type}?patient={patient_id} => {resp.status_code}")
        sys.stdout.flush()
        if resp.status_code == 404:
            return "not found", 404
        else:
            bundle = resp.json()
            print(bundle)
            cache.update_resource(resc_type, patient_id, bundle, curr_time)
            print(bundle)
            sys.stdout.flush()
            return bundle
    else:
        return {"resourceType":"Bundle", "entry": []}

    
def get_observation(patient_id):
    bundle = get_resource("Observation", patient_id)
    if bundle is None:
        return "not found", 404
    else:
        return bundle

                    
def get_condition(patient_id):
    bundle = get_resource("Condition", patient_id)
    if bundle is None:
        return "not found", 404
    else:
        return bundle


def post_patient(resource):
    cache.update_patient(resource, time.time())
    

def post_observation(resource):
    print(f"post observation {resource}")
    cache.post_resource(resource, time.time())


def post_condition(resource):
    cache.post_resource(resource, time.time())


def post_bundle(bundle):
    cache.post_bundle(bundle, time.time())


def delete_resource():
    cache.delete_resource()


