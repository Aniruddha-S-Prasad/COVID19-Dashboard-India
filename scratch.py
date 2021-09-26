# %%
import json
import numpy as np
import requests

# %%
api_url = 'https://data.covid19india.org/v4/min/timeseries.min.json'

state = 'KA'
time_series_response = json.loads(requests.get(api_url).text)
dates = list(time_series_response[state]['dates'].keys())

confirmed_delta = []
deceased_delta = []
recovered_delta = []
for date_str in dates:
    try:
        confirmed_delta.append(int(time_series_response[state]['dates'][date_str]['delta']['confirmed']))
    except KeyError:
        confirmed_delta.append(0)
    try:
        deceased_delta.append(int(time_series_response[state]['dates'][date_str]['delta']['deceased']))
    except KeyError:
        deceased_delta.append(0)
    try:
        recovered_delta.append(int(time_series_response[state]['dates'][date_str]['delta']['recovered']))
    except KeyError:
        recovered_delta.append(0)
    

confirmed_delta = np.array(confirmed_delta)
recovered_delta = np.array(recovered_delta)
deceased_delta = np.array(deceased_delta)
# %%
confirmed_total = np.cumsum(confirmed_delta)
recovered_total = np.cumsum(recovered_delta)
deceased_total = np.cumsum(deceased_delta)
# %%
