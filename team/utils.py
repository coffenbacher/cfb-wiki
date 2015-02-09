from helpers import sync_queries
from datetime import datetime
from dateutil.parser import parse

def extract_teams():
    queries = [{
      "connectorGuids": [
        "130b0529-37b9-4a5d-8963-a68307cff766"
      ],
      "input": {
        "webpage/url": "http://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_programs"
      }
    }]
    
    data = sync_queries(queries)
    tweaked = []
    for d in data:
        if 'joined_fbs' in d:
            d['joined_fbs'] = parse(d['joined_fbs/_utc']).isoformat()[:4]
        d['first_played'] = parse(d['first_played/_utc']).isoformat()[:4]
        tweaked.append(d)
    return data