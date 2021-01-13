import datetime
def defaultJsonEncoder(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
