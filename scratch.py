# %%
import json
import requests

# %%
api_url = 'https://data.covid19india.org/v4/min/timeseries.min.json'

time_series_response = json.loads(requests.get(api_url).text)
dates = time_series_response['TT']['dates'].keys()
len(list(time_series_response['TT']['dates'].keys()))
# %%
