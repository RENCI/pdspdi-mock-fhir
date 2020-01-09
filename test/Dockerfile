FROM python:3-alpine

RUN pip install requests pytest
RUN mkdir test

COPY test/test_pdspi_fhir_example.py /test/test_pdspi_fhir_example.py
COPY tx-utils/test /test
COPY pdsdpimockfhir/utils.py /test/pdsdpimockfhir/utils.py

WORKDIR test

ENTRYPOINT ["pytest"]

CMD ["-s"]

