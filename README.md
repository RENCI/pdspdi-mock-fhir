[![Build Status](https://travis-ci.com/RENCI/pdspi-fhir-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-fhir-example)

__Automated testing:__ The `./tests/test.sh` script is called by Travis (in .travis.yml, via hooks/test) with each commit to the master branch. Failing tests cause and update to the 'Build status' tag at the top of this file.

# "Files to FHIR Server" Appliance

- [Overview](#overview)
- [Appliance Setup](#appliance-setup)
- [Verify Setup](#verify-setup)
  + [Trouble Shooting](#trouble-shooting)
- [Deploy Appliance](#deploy-appliance)
- [Populate Appliance](#populate-appliance)
- [API doc and live example](#api-doc-and-live-example)

## Overview

This "Files to FHIR server" appliance can run stand-alone or
integrate into [PDS](http://github.com/RENCI/pds-release) development
stack. It can be used to serve FHIR data off disk (e.g., from Synthea),
serve PCORNet data as FHIR, or pass through data from another FHIR
server. Hence, this appliance allows the administrator to hot-swap FHIR
servers without modifying any code or configuration data on the FHIR
clients.

## Appliance Setup

1. Ensure prerequisites are met
    - Prerequisites
      - docker v19.03.14 or above
      - docker-compose 1.23.2 or above
 Refer to [doc/Docker.md](https://github.com/RENCI/pdspi-fhir-example/blob/master/doc/Docker.md) for help with installing docker, docker-compose, if needed.

2. Edit `tests/env.docker`:
    - `API_PORT` the port on which the FHIR server will be listening
    - `FHIR_SERVER_URL_BASE` an URL to a 3rd party FHIR server, if 'pass-through' functionality is desired. If the appliance is serving data off disk, set this variable to a dummy value.
    - The following can be provided arbitrary values in support of a database that will hold an internal representation of the patient data:
      - `MONGO_DATABASE` 
      - `MONGO_INITDB_ROOT_USERNAME`
      - `MONGO_INITDB_ROOT_PASSWORD`
      - `MONGO_NON_ROOT_USERNAME`
      - `MONGO_NON_ROOT_PASSWORD`
      - `MONGODB_DATA_VOLUME`
  
## Verify Setup

```
./tests/test.sh
```

### Trouble shooting

- If `docker` group was created and user was added to that group, `sudo` permission should not be required.
- If 404 error is encountered, ensure API_PORT is not already in use by another application, and that Appliance is not yet started
  ```
  netstat -tunlp
  docker ps
  ```

## Deploy Appliance

 - Start

```
./up.sh
```

 - Stop

_Note: Stopping the appliance will not free the attached docker volumes, hence the patient database will persist between deployment cycles unless epxlictly deleted._

```
./down.sh
```

## Populate Appliance 
_non-pass-through option_

If the appliance is not serving as a pass-through, it can be deployed
to serve stored data from a research data warehouse or a simulated
patient database. To serve data from storage, follow these steps to
have the appliance ingest the data.

1. Ensure prerequistes are met
    - Prerequisites 
      - Python 3.8 or above
      - Python libraries: pandas, tx-functional, joblib, tqdm, requests, python-dateutil
 Refer to [doc/Python.md](http://github.com/RENCI/pdspi-fhir-example/blob/master/doc/Python.md) for help with installing python 3.8 and libraries, if needed.

2. Ensure the FHIR server appliance container is running

  ```
  docker ps # look for containers started by ./up.sh
  ```

3. Ingest patient data

To ingest FHIR data from disk, run:

  ```
  PYTHONPATH=tx-utils/src python ingest.py <base_url> <input_dir>
  ```

To ingest PCORNet data, run:

  ```
  PYTHONPATH=tx-utils/src:tx-pcornet-to-fhir/ python ingest.py --base_url <base_url> --input_dir <pcori_data_input_dir> --input_data_format pcori --output_dir <pcori_data_output_dir>
  ```

For example, PCORNet ingestion might look like this: 

  ```
   PYTHONPATH=tx-utils/src:tx-pcornet-to-fhir/ python ingest.py --base_url http://localhost:8080 --input_dir 1000-null --input_data_format pcori --output_dir 1000-out
  ```

## API doc and live example

- Docker image built from latest commit to master

`txscience/pdspi-fhir-example:unstable`

Each commit to master triggers a build on dockerhub, tagged with 'unstable'. This image can be run in lieue of `./up.sh`, provided the appropriate environemetnal variables such as those found in `tests/env.docker`.

- API documentation

`http://pds.renci.org:8080/v1/plugin/pdspi-fhir-example/ui/`
