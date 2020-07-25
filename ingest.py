import sys
import os
import json
import requests
import logging
from tx.fhir.utils import bundle, unbundle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url, input_dir = sys.argv[1:]

for root, _, files in os.walk(input_dir, followlinks=True):
    for file in files:
        path = f"{root}/{file}"
        with open(path) as input_stream:
            logging.info(f"loading {path}")
            obj = json.load(input_stream)
            rescs = unbundle(obj).value
            nrescs = len(rescs)
            logging.info(f"{nrescs} resources loaded")
            maxlen = 1024
            for i in range(0, nrescs, maxlen):
                subrescs = rescs[i: min(i+maxlen, nrescs)]
                subobj = bundle(subrescs)
                logging.info(f"ingesting {path} {i}")
                requests.post(f"{base_url}/Bundle", json=subobj)
