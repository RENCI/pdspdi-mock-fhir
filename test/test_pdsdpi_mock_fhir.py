import requests
import time
import ndjson

def test_logging():

    resp1 = requests.post("http://txlogging:8080/log", json={
        "event":"this is an event",
        "timestamp": "2001-01-01",
        "comments":"this is a comments"
    })
    
    assert resp1.status_code == 200

    time.sleep(10)

    resp2 = requests.get("http://txlogging:8080/log", params={
    })

    assert resp2.status_code == 200
    assert len(ndjson.loads(resp2.text)) == 1

    start = "2001-01-01"
    end = "2002-01-01"

    resp3 = requests.get("http://txlogging:8080/log", params={
        "start": start,
        "end": end
    })

    assert resp3.status_code == 200
    assert len(ndjson.loads(resp3.text)) == 1

    start = "2002-01-01"
    end = "2003-01-01"

    resp4 = requests.get("http://txlogging:8080/log", params={
        "start": start,
        "end": end
    })

    assert resp4.status_code == 200
    assert len(ndjson.loads(resp4.text)) == 0
