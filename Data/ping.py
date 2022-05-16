import requests
import json

uri = "https://endpoint.on.azure.net/score"
print(uri)

headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key":"YOUR-KEY"}
json_input = '''[20220505, 20220506, 20220507]'''
response = requests.post(uri, data=json_input, headers=headers)

"""
#datesToSend = [20220505, 20220506, 20220507] 
response = requests.post(uri, data=json.dumps(datesToSend), headers=headers) 
"""

assert response.status_code == 200
print(response.text)

#IF response is data frame:
"""
import pandas as pd

df = pd.read_json(response.text)
print(df.shape)
"""