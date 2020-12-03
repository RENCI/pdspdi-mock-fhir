FROM python:3-alpine

RUN pip install requests pytest
RUN mkdir test

COPY test/hapi-fhir/test_hapi_fhir.py /test/test_hapi_fhir.py
COPY pdsdpimockfhir/utils.py /test/pdsdpimockfhir/utils.py

WORKDIR test

ENTRYPOINT ["pytest"]

CMD ["-s"]

