[![Build Status](https://travis-ci.com/RENCI/pdspi-fhir-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-fhir-example)
# pdspi-fhir-example

### set up
edit `tests/docker.env`

`API_PORT` the port mapped for host

### start

```
./up.sh
```

### stop
```
./down.sh
```

### ingest

- Prerequisites 
  	- Python 3.8 or above
  	- `pip install` these libraries: Pandas, tx-functional, joblib, and tqdm libraries need to be installed in the python 3.8 environment where ingest.py runs.
    - Make sure the FHIR server is running first (./up.sh)
- To ingest fhir data, run:

```
PYTHONPATH=tx-utils/src python ingest.py <base_url> <input_dir>
```

- To ingest pcori data, run:

  ```
  PYTHONPATH=tx-utils/src:tx-pcornet-to-fhir/ python ingest.py --base_url <base_url> --input_dir <pcori_data_input_dir> --input_data_format pcori --output_dir <pcori_data_output_dir>
  ```
  For example: 
  ```
   PYTHONPATH=tx-utils/src:tx-pcornet-to-fhir/ python ingest.py --base_url http://localhost:8080 --input_dir 1000-null --input_data_format pcori --output_dir 1000-out
  ```

### test

```
test/test.sh
```

### API doc and live example
http://pds.renci.org:8080/v1/plugin/pds-data-provider-mock-fhir/ui/
