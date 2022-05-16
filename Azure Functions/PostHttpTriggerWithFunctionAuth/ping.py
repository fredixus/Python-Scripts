import requests
import json

uri = "http://localhost:7071/api/PostHttpTrigger"
print(uri)

headers = {"Content-Type": "application/json", "x-function-key":"YOUR-KEY"}
json_input = {'dates':'["20220505", "20220506", "20220507"]','type':'custom %Y/%M/%d'}
response = requests.post(uri, data=json.dumps(json_input), headers=headers)

assert response.status_code == 200
print(response.text)

