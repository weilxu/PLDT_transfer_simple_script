import pynautobot
import pandas as pd
import requests

#nb = pynautobot.api("http://10.66.69.149:8481", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

    
source = pd.ExcelFile('mastersheet_sharepoint_status_santized.xlsx')

site_df = pd.read_excel(source, 'PORT_MAPPING')

headers = {
    'Authorization': 'Token b7d568b9a5a400a249a057fca8a2b0d6dcc05828',
    'Content-Type': 'application/json',
    'Accept': 'application/json; indent=4',
}
duplicate_list = []

nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/cables/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")
#255s
#
for idx in range(0,len(site_df['hostname'])):

    name = site_df['hostname'][idx]
    print(name)

    interface = site_df['interface'][idx]
    print(interface)

    rname = site_df['remote_hostname'][idx]
    print(rname)

    rinterface = (site_df['remote_interface'][idx])
    print(rinterface)


    dup = f'{name}_{interface}'
    rdup = f'{rname}_{rinterface}'

    if dup in duplicate_list:
        continue
    elif rdup in duplicate_list:
        continue
    else:
        duplicate_list.append(dup)
        duplicate_list.append(rdup)


        while True:
            try:
                response = requests.get(f'http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?device={name}&name={interface}', headers=headers)
                break
            except:
                continue


        parse = response.json()

        
        for x in parse['results']:
            id = x['id']
            id_dev = x['device']['id']
            break
        
        print(id)
        print(id_dev)


        while True:
            try:
                rresponse = requests.get(f'http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?device={rname}&name={rinterface}', headers=headers)
                break
            except:
                continue


        rparse = rresponse.json()

        



        for y in rparse['results']:
            rid = y['id']
            rid_dev = y['device']['id']
            break
        print(rid)
        print(rid_dev)

        print(duplicate_list)

    
        
        try:
            nb.dcim.cables.create([
                {   
                    "termination_a_type": "dcim.interface",
                    "termination_a_id": id,
                    "termination_a": {
                        "id": id,
                        "device": {
                            "type" : "interface",
                            "id": id_dev,
                            "name": name,
                            "display_name": name
                        },
                        "name": interface,
                        "cable": "c1332e55-3a6d-4e79-8331-6a9d8d5755da",
                    },
                    "termination_b_type": "dcim.interface",
                    "termination_b_id": rid,
                    "termination_b": {
                        "id": rid,
                        "device": {
                            "type" : "interface",
                            "id": rid_dev,
                            "name": rname,
                            "display_name": rname
                        },
                        "name": rinterface,
                    },
                    "type": "",
                    "status": "in-use",
                    "label": "",
                    "color": "",
                    "tags": [
                        {
                            "name": "INFRA",
                            "slug": "infra",
                        }
                    ],
                    "custom_fields": {}
                }
            ])

        except:
            continue

