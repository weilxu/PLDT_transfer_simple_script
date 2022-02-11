import pynautobot
import pandas as pd
import requests

#nb = pynautobot.api("http://10.66.69.149:8481", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

    
source = pd.ExcelFile('mastersheet_sharepoint_status_santized.xlsx')

site_df = pd.read_excel(source, 'DEVICE_INFORMATION')

nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/ipam/ip-addresses/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

headers = {
    'Authorization': 'Token b7d568b9a5a400a249a057fca8a2b0d6dcc05828',
    'Content-Type': 'application/json',
    'Accept': 'application/json; indent=4',
}

#len(site_df['hostname']
#for idx in range(0,len(site_df['hostname'])):
for idx in range(0,len(site_df['hostname'])):

    name = site_df['hostname'][idx]
    print(name)
    interface = 'Loopback0'
    print(interface)
    ipv4 = site_df['lo0_ipv4'][idx]
    ipv4 = ipv4.split(' ')
    ipv4 = ipv4[0]
    ipv4 = f"{ipv4}/32"
    print(ipv4)
    ipv6 = site_df['lo0_ipv6'][idx]
    print(ipv6)

    while True:
        try:
            response = requests.get(f'http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?device={name}&name={interface}', headers=headers)

            parse = response.json()
            break
        except ValueError:
            break
        except:
            continue
    



    for x in parse['results']:
        id = 0
        device = x['device']['name']
        be = x['name']
        if device == name and be == interface:
            id = x['id']
            break
        else:
            continue
  
    print(id)
    print('*****')
    if id == 0:
        continue
    else:
        pass
    
    while True:
        try:
            nb.ipam.ip_addresses.create([
                        {

                            "family": {
                                "value": 4,
                                "label": "IPv4"
                            },
                            "address": ipv4,
                            "status":  "In-use",
                            "role" : "loopback",
                            "assigned_object_type": "dcim.interface",
                            "assigned_object_id": id,
                            "assigned_object": {
                                "device": {
                                    "name": name,
                                    "display_name": name
                                },
                                "name": interface,
                            },
                            "dns_name": "",
                            "description": "",
                            "tags": [{"name": "Lo0"}],
                            "custom_fields": {}
                        }
                    

            ])
            break
        except ValueError:
            break
        except:
            continue

    print(type(ipv6))
    print(ipv6)
    if type(ipv6) == float:
        continue
    else:
        while True:
            try:
                nb.ipam.ip_addresses.create([
                    
                            {

                                "family": {
                                    "value": 6,
                                    "label": "IPv6"
                                },
                                "address": ipv6,
                                "status":  "In-use",
                                "role" : "loopback",
                                "assigned_object_type": "dcim.interface",
                                "assigned_object_id": id,
                                "assigned_object": {
                                    "device": {
                                        "name": name,
                                        "display_name": name
                                    },
                                    "name": interface,
                                },
                                "dns_name": "",
                                "description": "",
                                "tags": [{"name": "Lo0"}],
                                "custom_fields": {}
                            }
                        

                ])
                break
            except ValueError:
                break
            except:
                continue