# This program takes the input from user and update the attriutes of that interface
# ################################################################################### 

import requests
import json
import sys

device = json.loads(open("device_login.json").read())
module = 'ietf-interfaces:interfaces'
url = f"https://{device['host']}/restconf/data/"
requests.packages.urllib3.disable_warnings()

def get_interfaces():
    interface_list=[]
    response_get = requests.get(f"{url}{module}", headers=device['headers'], auth=(device['username'], device['password']), verify=False).json()
    interfaces_list = response_get['ietf-interfaces:interfaces']['interface']
    for interface_detail in interfaces_list:
        interface_list.append(interface_detail["name"])
    return interface_list

###########################################################    

def get_interface_name(interface_list):
    intname = None
    while intname is None:
        int_name = input("\nEnter the interface name you want to update : ")
        for intf_name in interface_list:
            if int_name.lower() == intf_name.lower():
                intname = intf_name
                break
        if intname is not None:
            return intname
        else:
            print("invalid interface / Enter the name in same format")
            continue

###########################################################    
       
def get_interface_details(int_name):
    interface_detail = requests.get(f"{url}{module}/interface={int_name}", headers=device['headers'], auth=(device['username'], device['password']), verify=False).json()['ietf-interfaces:interface']
    print(f"Name : {interface_detail['name']}")
    if 'description' in interface_detail.keys():
        print(f"Description : {interface_detail['description']}")
    print(f"Type : {interface_detail['type']}")
    if bool(interface_detail['ietf-ip:ipv4']):
        for i in range(0, len(interface_detail['ietf-ip:ipv4']['address'])):
            print(f"IP Address : {interface_detail['ietf-ip:ipv4']['address'][i]['ip']}")
            print(f"Subnet Mask : {interface_detail['ietf-ip:ipv4']['address'][i]['netmask']}")

###########################################################    

def get_attribute():
    while True:
        attr_name = input("\nEnter the attribute you want to update : ").lower()  
        if attr_name == 'description' or attr_name == 'ip address':
            return attr_name          
        else:
            print("invalid selction / Enter the attribute in same format")
            continue

###########################################################    
        
def update_interface(attr_name, int_name):
    if attr_name == 'description':
        desc = input("\nEnter the description you want to update : ")
        data_filter = { 
                "ietf-interfaces:interface": {
                    "name": desc
                } }
        return requests.patch(f"{url}{module}/interface={int_name}", headers=device['headers'], auth=(device['username'], device['password']), verify=False, data=json.dumps(data_filter)).status_code
    else:
        ip = input("\nEnter the ip address : ")
        int_details = requests.get(f"{url}{module}/interface={int_name}", headers=device['headers'], auth=(device['username'], device['password']), verify=False).json()
        int_details['ietf-interfaces:interface']['ietf-ip:ipv4']['address'][0]['ip'] = ip
        return requests.put(f"{url}{module}/interface={int_name}", headers=device['headers'], auth=(device['username'], device['password']), verify=False, data=json.dumps(int_details)).status_code

###########################################################    
     
def main():
    interface_names = get_interfaces()    
    print("\nBelow the interfaces configured in the router :")
    for i, interface in enumerate(interface_names):
        print(f'{i+1}: {interface}')
    interface_name = get_interface_name(interface_names)
    print(f'\nBelow are the details for interface {interface_name} :\n')
    get_interface_details(interface_name)
    print(f'\nBelow are the attributes of interface {interface_name} :')
    print("1: description  2: ip address")
    attribute_name = get_attribute()
    response_code = update_interface(attribute_name, interface_name)
    if response_code == 204:
        print(f'Update successfully ')
    else:
        print(f'respone code : {response_code}. Update failed')
        
if __name__ == '__main__':
    sys.exit(main())
