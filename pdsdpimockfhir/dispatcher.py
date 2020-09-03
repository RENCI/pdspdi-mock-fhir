import os
import copy
from pymongo import MongoClient
from flask import Response, send_file
from bson.json_util import dumps
import logging
import time
import pdsdpimockfhir.cache as cache
import requests
import sys
from joblib import Parallel, delayed
from urllib.parse import urlsplit
from tx.fhir.utils import bundle, unbundle
from tx.functional.either import Left, Right
import tx.functional.maybe as maybe
from tx.functional.utils import identity
from tx.logging.utils import getLogger
import multiprocessing
from multiprocessing import Process, Manager
from tempfile import mkstemp
from functools import partial
import json

logger = getLogger(__name__, logging.INFO)


fhir_server_url_base = os.environ.get("FHIR_SERVER_URL_BASE")


def _get_patient(patient_id):
    resc = cache.get_patient(patient_id)

    if resc is not None:
        return resc
    elif fhir_server_url_base is not None and fhir_server_url_base != "":
        resp = requests.get(f"{fhir_server_url_base}/Patient/{patient_id}")
        if resp.status_code == 404:
            return None
        else:
            resc = resp.json()
            cache.update_patient(resc)
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
    resources = cache.get_resource(resc_type, patient_id)

    if resources is not None and resources["entry"] != []:
        return resources
    elif fhir_server_url_base is not None and fhir_server_url_base != "":
        resp = requests.get(f"{fhir_server_url_base}/{resc_type}?patient={patient_id}")
        logger.debug(f"{fhir_server_url_base}/{resc_type}?patient={patient_id} => {resp.status_code}")
        if resp.status_code == 404:
            return None
        else:
            resources = resp.json()
            cache.update_resource(resc_type, patient_id, resources)
            return resources
    else:
        return bundle([])

    
def post_resources(resc_types, patient_ids):
    patients = []
    def proc(p, patient_id):
        index, patient_id = patient_id
        logger.info(f"processing patient {index} {patient_id}")
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
        q.put(patient)

    n_jobs = maybe.from_python(os.environ.get("N_JOBS")).bind(int).rec(identity, multiprocessing.cpu_count())

    def save_to_file(tmpfile, q):
        with open(tmpfile, 'w') as out:
            first = True
            out.write("[\n")
            while True:
                val = q.get()
                if val is None:
                    break
                if first:
                    first = False
                else:
                    out.write(",\n")
                out.write(json.dumps(val))
            out.write("]\n")

    with Manager() as m:
        q = m.Queue()
        fd, tmpfile = mkstemp()
        os.close(fd)
        try:
            p = Process(target=save_to_file, args=(tmpfile, q))
            p.start()
            Parallel(n_jobs=n_jobs)(delayed(partial(proc, q))(patient_id) for patient_id in enumerate(patient_ids))
            q.put(None)
            p.join()
        
            logger.info(f"finished processing patients")
            return send_file(tmpfile)
        except:
            os.remove(tmpfile)
            raise


def get_resource(resource_name, patient_id):
    bundle = _get_resource(resource_name, patient_id)
    if bundle is None:
        return "not found", 404
    else:
        return bundle

                    
def post_patient(resource):
    cache.update_patient(resource)
    return "success", 200
    

def post_resource(resource):
    cache.post_resource(resource)
    return "success", 200


def post_batch(batch):
    return _post_batch(batch).rec(lambda x: (x, 500), lambda x: x)


def _post_batch(batch):
    def handle_requests(requests):
        rescs = []
        for request in requests:
            logger.info(f"processing request {request}")
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
    cache.post_bundle(bundle)
    return "success", 200


def delete_resource():
    cache.delete_resource()
    return "success", 200


