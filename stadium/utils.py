from helpers import sync_queries
from datetime import datetime
from dateutil.parser import parse

def extract_stadiums():
    queries = [{
      "connectorGuids": [
        "915c814c-912c-4236-bdb4-e4acbe48ce13"
      ],
      "input": {
        "webpage/url": "http://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_stadiums"
      }
    }]
    
    data = sync_queries(queries)
    tweaked = []

    for d in data:
        if 'built_datetime' in d and isinstance(d['built_datetime'],int):
            d['built_datetime'] = parse(d['built_datetime/_utc']).isoformat()[:4]
        if 'record_datetime' in d and isinstance(d['record_datetime'],int):
            d['record_datetime'] = parse(d['record_datetime/_utc']).isoformat()[:4]
        d['capacity'] = int(d['capacity'].replace(',', ''))
        if 'record' in d:
            d['record'] = int(d['record'].replace(',', ''))
        tweaked.append(d)
        
    return data