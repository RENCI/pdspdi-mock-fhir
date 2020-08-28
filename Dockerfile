FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk add --no-cache gcc musl-dev libffi-dev file make
RUN pip3 install --no-cache-dir flask pymongo gunicorn[gevent]==19.9.0 connexion[swagger-ui] requests flask-cors tx-functional python-dateutil

COPY api /usr/src/app/api
COPY pdsdpimockfhir /usr/src/app/pdsdpimockfhir
COPY tx-utils/src /usr/src/app

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "--error-logfile", "-", "--capture-output", "-t", "100000", "api.server:create_app()"]
