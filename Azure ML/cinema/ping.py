import requests
import json

uri = 'http://localhost:6789/score'

headers = {"Content-Type": "application/json"}

inputs = {
    'cashiers':1, 
    'servers':5, 
    'ushers':10
}

response = requests.post(uri, data=json.dumps(inputs), headers=headers)

#print(json.dumps(inputs))

print(response.json())