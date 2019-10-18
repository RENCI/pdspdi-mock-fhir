import sys

def bundle(records):
    return {
        "resourceType": "Bundle",
        "entry": list(map(lambda record: {
            "resource": record
        }, records))
    }

def unbundle(bundle):
    print(f"bundle={bundle}, bundle.keys()={bundle.keys()}")
    sys.stdout.flush()
    return list(map(lambda a : a["resource"], bundle.get("entry", [])))


