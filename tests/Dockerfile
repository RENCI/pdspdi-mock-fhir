FROM python:3-alpine

RUN pip install requests pytest tx-functional
RUN mkdir test

COPY tests/test_pdspi_fhir_example.py /test/test_pdspi_fhir_example.py
# COPY tx-utils/test /test
COPY tx-utils/src /test

WORKDIR test

ENTRYPOINT ["pytest"]

CMD ["-s"]

