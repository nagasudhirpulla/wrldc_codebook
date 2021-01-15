import datetime
from flask.json import JSONEncoder


def defaultJsonEncoder(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


class ServerJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
