import json


def getConfig(fName: str = "config.json") -> dict:
    with open(fName) as f:
        data = json.load(f)
        return data
