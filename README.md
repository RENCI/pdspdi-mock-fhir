# pdspdi-mock-fhir

### run

```
docker-compose -f docker-compose.yml up --build
```

### test
```
docker-compose -f docker-compose.yml -f test/docker-compose.yml up --build -V --exit-code-from txlogging-test
```
