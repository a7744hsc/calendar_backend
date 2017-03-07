from flask.json import JSONEncoder
from datetime import date, datetime

class CustomJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        return JSONEncoder.default(self, o)
