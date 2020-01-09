#!/bin/bash
docker-compose -f docker-compose.yml -f volume/docker-compose.yml -f test/docker-compose.yml up --build -V --exit-code-from pdspi-fhir-example-test
