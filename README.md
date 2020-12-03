0;136;0c[![Build Status](https://travis-ci.com/RENCI/pdspi-fhir-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-fhir-example)
### Automated testing
The `./test.sh` script is called by Travis (in .travis.yml, via hooks/test) with each commit to the master branch. Failing tests cause and update to the 'Build status' tag at the top of this file.

# "Files to FHIR Server" Appliance

- [Overview](#overview)
- [Appliance Setup](#appliance-setup)
- [Verify Setup](#verify-setup)
  + [Trouble Shooting](#trouble-shooting)
- [Deploy Appliance](#start-appliance)
- [Populate Appliance](#populate-appliance)
- [API doc and live example](#api-doc-and-live-example)

## Overview

This "files to FHIR server" appliance can run stand-alone or
integrates into [PDS](http://github.com/RENCI/pds-release) development
stack. Can be used to serve FHIR data off disk (e.g., from Synthea),
serve PCORNet data as FHIR, or pass through data from another FHIR
server. This appliance allows the administrator to hot-swap FHIR
servers without modifying any code or configuration data on the FHIR
clients.

## Appliance Setup

1. Ensure prerequisites are met
  - Prerequisites
    - docker v19.03.14 or above
    - docker-compose 1.23.2 or above
 Refer to [doc/Docker.md](http://github.com/RENCI/pdspi-fhir-example/doc/Docker.md) for help with installing docker, docker-compose, if needed.

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
__Note: Stopping the appliance will not free the attached docker volumes, hence the patient database will persist between deployment cycles unless epxlictly deleted.__ 
```
./down.sh
```

## Populate Appliance 
__non-pass-through option__

If the appliance is not serving as a pass-through, it can be deployed
to serve stored data from a research data warehouse or a simulated
patient database. To serve data from storage, follow these steps to
have the appliance ingest the data.

1. Ensure prerequistes are met
  - Prerequisites 
  	- Python 3.8 or above
  	- Python libraries: pandas, tx-functional, joblib, tqdm, requests, python-dateutil
 Refer to [doc/Python.md](http://github.com/RENCI/pdspi-fhir-example/doc/Python.md) for help with installing python 3.8 and libraries, if needed.

2. Ensure the FHIR server appliance container is running

  ```
  docker ps # look for containers started by ./up.sh
  ```

3. Ingest patient data

  ```
  PYTHONPATH=tx-utils/src python ingest.py <base_url> <input_dir>
  ```

To ingest PCORNet data, run:

  ```
  PYTHONPATH=tx-utils/src:tx-pcornet-to-fhir/ python ingest.py --base_url <base_url> --input_dir <pcori_data_input_dir> --input_data_format pcori --output_dir <pcori_data_output_dir>
  ```

For example: 

  ```
   PYTHONPATH=tx-utils/src:tx-pcornet-to-fhir/ python ingest.py --base_url http://localhost:8080 --input_dir 1000-null --input_data_format pcori --output_dir 1000-out
  ```

## API doc and live example

- Docker image built from latest commit to master
`txscience/pdspi-fhir-example:unstable`
Each commit to master triggers a build on dockerhub, tagged with 'unstable'. This image can be run in lieue of `./up.sh, provided the appropriate environemetnal variables such as those found in `tests/env.docker`.

- API documentation
`http://pds.renci.org:8080/v1/plugin/pdspi-fhir-example/ui/`
