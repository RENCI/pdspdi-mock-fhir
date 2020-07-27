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
from urllib.parse import urlsplit
from tx.fhir.utils import bundle, unbundle
from tx.functional.either import Left, Right
from .utils import getLogger


fhir_server_url_base = os.environ.get("FHIR_SERVER_URL_BASE")


logger = getLogger(__name__)


def _get_patient(patient_id):
    resc = cache.get_patient(patient_id)

    if resc is not None:
        return resc
    elif fhir_server_url_base is not None and fhir_server_url_base != "":
        curr_time = time.time()
        resp = requests.get(f"{fhir_server_url_base}/Patient/{patient_id}")
        if resp.status_code == 404:
            return None
        else:
            resc = resp.json()
            cache.update_patient(resc, curr_time)
            return resc
    else:
        return None
        

def get_patient(patient_id):
    resc = _get_patient(patient_id)

    if resc is not None:
        return resc
    else:
        return "not found", 404
        

def _get_resource(resc_type, patient_id):
    bundle = cache.get_resource(resc_type, patient_id)

    if bundle is not None:
        return bundle
    elif fhir_server_url_base is not None and fhir_server_url_base != "":
        curr_time = time.time()
        resp = requests.get(f"{fhir_server_url_base}/{resc_type}?patient={patient_id}")
        logger.debug(f"{fhir_server_url_base}/{resc_type}?patient={patient_id} => {resp.status_code}")
        if resp.status_code == 404:
            return None
        else:
            bundle = resp.json()
            print(bundle)
            cache.update_resource(resc_type, patient_id, bundle, curr_time)
            print(bundle)
            sys.stdout.flush()
            return bundle
    else:
        return {"resourceType":"Bundle", "entry": []}

    
def post_resources(resc_types, patient_ids):
    patients = []
    for patient_id in patient_ids:
        requests = []
        for resc_type in resc_types:
            if resc_type == "Patient":
                requests.append({
                    "url": f"/Patient/{patient_id}",
                    "method": "GET"
                })
            else:
                requests.append({
                    "url": f"/{resc_type}?patient={patient_id}",
                    "method": "GET"
                })
        batch = bundle(requests, "batch")
        patient = _post_batch(batch).value
        patients.append(patient)
    return patients                


def get_resource(resource_name, patient_id):
    bundle = _get_resource(resource_name, patient_id)
    if bundle is None:
        return "not found", 404
    else:
        return bundle

                    
def post_patient(resource):
    cache.update_patient(resource, time.time())
    return "success", 200
    

def post_resource(resource):
    cache.post_resource(resource, time.time())
    return "success", 200


def post_batch(batch):
    return _post_batch(batch).rec(lambda x: (x, 500), lambda x: x)


def _post_batch(batch):
    def handle_requests(requests):
        rescs = []
        for request in requests:
            method = request["method"]
            url = request["url"]
            result = urlsplit(url)
            pcs = result.path.split("/")
            qcs = map(lambda x: x.split("="), result.query.split("&"))
            if pcs[1] == "Patient":
                rescs.append(_get_patient(pcs[2]))
            else:
                patient_id = None
                for qc in qcs:
                    if qc[0] == "patient":
                        patient_id = qc[1]
                rescs.append(_get_resource(pcs[1], patient_id))
        return Right(bundle(rescs, "batch-response"))

    return unbundle(batch).bind(handle_requests)


def post_bundle(bundle):
    cache.post_bundle(bundle, time.time())
    return "success", 200


def delete_resource():
    cache.delete_resource()
    return "success", 200


