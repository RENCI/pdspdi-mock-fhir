FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk add --no-cache gcc musl-dev libffi-dev file make
RUN pip3 install --no-cache-dir flask pymongo greenlet==0.4.16 gevent==1.4.0 gunicorn[gevent]==19.9.0 connexion[swagger-ui] requests flask-cors tx-functional python-dateutil pathvalidate==2.3.0

COPY api /usr/src/app/api
COPY pdsdpimockfhir /usr/src/app/pdsdpimockfhir
COPY tx-utils/src /usr/src/app

EXPOSE 8080

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "--error-logfile", "-", "--capture-output", "api.server:create_app()"]

CMD ["-w", "4", "-t", "100000"]
