import requests
import json

device = json.loads(open("device_login.json").read())
module = 'ietf-interfaces:interfaces'
url = f"https://{device['host']}/restconf/data"
payload = json.dumps({"Cisco-IOS-XE-native:hostname": "csr1000v-1"})

requests.packages.urllib3.disable_warnings()
# response_put = requests.put(f"{url}/{module}", headers=device['headers'], auth=(device['username'], device['password']),
#                             verify=False, data=payload)

response_get = requests.get(f"{url}/{module}", headers=device['headers'], auth=(device['username'], device['password']),
                            verify=False).json()
# print(json.dumps(response_get))