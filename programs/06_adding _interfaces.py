import requests
import json

device = json.loads(open("device_login.json").read())
module = 'ietf-interfaces:interfaces/interface'
url = f"https://{device['host']}/restconf/data/"
data_filter ={ 
    "ietf-interfaces:interface": {
        "name": "Loopback",
        "description": "",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
          "address": [
            {
              "ip": "",
              "netmask": "255.255.255.0"
            }
          ]
        },
        "ietf-ip:ipv6": {}
      }
    }

int_name = data_filter["ietf-interfaces:interface"]['name']
requests.packages.urllib3.disable_warnings()

for int_number in range(101,105):
    data_filter["ietf-interfaces:interface"]["name"] = f'{int_name}{int_number}'
    data_filter["ietf-interfaces:interface"]["description"] = f'{data_filter["ietf-interfaces:interface"]["name"]} configured by RESTCONF-ERAGON'
    data_filter["ietf-interfaces:interface"]["ietf-ip:ipv4"]["address"][0]["ip"] = f'10.20.30.{int_number}'
    payload = json.dumps(data_filter)
    print(payload)
    
    response_post = requests.patch(f"{url}{module}", headers=device['headers'], auth=(device['username'], device['password']), verify=False, data=payload)
    print(response_post.text)

response_get = requests.get(f"{url}{module}", headers=device['headers'], auth=(device['username'], device['password']), verify=False).json()

# print(response_post.text)
print(response_get)