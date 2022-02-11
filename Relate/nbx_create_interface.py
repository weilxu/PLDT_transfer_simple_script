import pynautobot
import pandas as pd


#nb = pynautobot.api("http://10.66.69.149:8481", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

    
source = pd.ExcelFile('mastersheet_sharepoint_status_santized.xlsx')

site_df = pd.read_excel(source, 'PORT_MAPPING')


nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")
#255s
#
for idx in range(0,len(site_df['hostname'])):

    name = site_df['hostname'][idx]
    print(name)
    interface = (site_df['interface'][idx])
    print(interface)
    int_type = site_df['type'][idx]
    print(int_type)
    bundle = site_df['bundle'][idx]
    print(bundle)
    isis = site_df['isis'][idx]
    int_desc = (site_df['interface_description'][idx])
    
    if len(int_desc) > 200:
        new_desc = ''
        for x in range(0,200):
            new_desc = new_desc + int_desc[x]
        int_desc = new_desc
    else:
        pass
    print(int_desc)
    
    while True:
        try:
            nb.dcim.interfaces.create([
                {
                    "device": {"name": name},
                    "name" : interface,
                    "type" : int_type,
                    "description": int_desc,
                    "lag" : {'name':bundle, 'device':{"name": name}},
                    "custom_fields": {"Endpoint-Type": "INFRA","Isis-Domain": isis}

                }
            ])
            break

        except ValueError:
            break
        except:
            continue

