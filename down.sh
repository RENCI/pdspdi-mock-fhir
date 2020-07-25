#!/bin/bash

set -o allexport
source env.TAG
source test/env.docker
set +o allexport

docker-compose -f docker-compose.yml -f volume/docker-compose.yml down
