FROM python:3-alpine

RUN pip install requests pytest
RUN mkdir test

COPY test_pdsdpi_mock_fhir.py /test/test_pdsdpi_mock_fhir.py

WORKDIR test

ENTRYPOINT ["pytest"]

CMD ["-s"]

