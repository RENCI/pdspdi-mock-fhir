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
```
PYTHONPATH=tx-utils/src python ingest.py <base_url> <input_dir>
```

### test

```
test/test.sh
```

### API doc and live example
http://pds.renci.org:8080/v1/plugin/pds-data-provider-mock-fhir/ui/
