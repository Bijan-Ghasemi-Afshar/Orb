import requests
import json

# Documentation can be found at
#   https://wiki.openraildata.com/index.php/HSP

# When registering at https://datafeeds.nationalrail.co.uk/
# you only need the HSP subscription
# The Real time Data feed is too much to deal with
# The On Demand Data Feeds might be useful
# 
# In 'Planned usage', mention you are using the HSP data 
# for educational purposes, for a project, and for a limited
# time
# The T & Cs should not be an issue, nor the limit on the
# number of requests an hour - but do be polite and do not
# swamp the web service with an excessive number of requests

api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
# api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

headers = { "Content-Type": "application/json" }
auths = ("b.ghasemi-afshar@uea.ac.uk", "ORBcoursework18%")

data = {
  "from_loc": "NRW",
  "to_loc": "LST",
  "from_time": "0000",
  "to_time": "2359",
  "from_date": "2018-11-12",
  "to_date": "2018-11-16",
  "days": "WEEKDAY",
  "tolerance": ["10", "60"]
}

# data = {
#     "rid":"201811157681034"
# }

r = requests.post(api_url, headers=headers, auth=auths, json=data)

print(json.dumps(json.loads(r.text), sort_keys=True, indent=2, separators=(',',': ')))
