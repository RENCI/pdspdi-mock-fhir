import sys
import os
import json
import requests
import logging
from tx.fhir.utils import bundle, unbundle
from tx.logging.utils import getLogger
from joblib import Parallel, delayed
from functools import partial

threads, base_url, input_dir = sys.argv[1:]

num_threads = int(threads)

paths = [f"{root}/{file}" for root, _, files in os.walk(input_dir, followlinks=True) for file in files]



def handle_path(path):
    logger = getLogger(f"{__name__}{os.getpid()}", logging.INFO)

    with open(path) as input_stream:
        logger.info(f"loading {path}")
        obj = json.load(input_stream)
        rescs = unbundle(obj).value
        nrescs = len(rescs)
        logger.info(f"{nrescs} resources loaded")
        maxlen = 1024
        for i in range(0, nrescs, maxlen):
            subrescs = rescs[i: min(i+maxlen, nrescs)]
            subobj = bundle(subrescs)
            logger.info(f"ingesting {path} {i}")
            requests.post(f"{base_url}/Bundle", json=subobj)

Parallel(n_jobs=num_threads)(delayed(handle_path)(path) for path in paths)
