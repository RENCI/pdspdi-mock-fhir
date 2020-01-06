FROM python:3-alpine

RUN pip install requests pytest
RUN mkdir test

COPY test/test_pdsdpi_mock_fhir.py /test/test_pdsdpi_mock_fhir.py
COPY tx-utils/test /test
COPY pdsdpimockfhir/utils.py /test/pdsdpimockfhir/utils.py

WORKDIR test

ENTRYPOINT ["pytest"]

CMD ["-s"]

