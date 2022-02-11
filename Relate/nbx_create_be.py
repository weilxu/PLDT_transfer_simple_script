import pynautobot
import pandas as pd



    
source = pd.ExcelFile('mastersheet_sharepoint_status_santized.xlsx')

site_df = pd.read_excel(source, 'PORT_MAPPING_BE')
nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

#len(site_df['hostname'])

for idx in range(0,len(site_df['hostname'])):

    name = site_df['hostname'][idx]
    print(name)
    bundle = site_df['bundle'][idx]
    print(bundle)
    isis = site_df['isis'][idx]
    print(isis)
    be_desc = site_df['bundle_description'][idx]
    print(be_desc)
    




    while True:
        try:
            nb.dcim.interfaces.create([
                {
                    "device": {"name": name},
                    "name" : bundle,
                    "type" : 'lag',
                    "description": be_desc,
                    "custom_fields": {"Endpoint-Type": "INFRA","Isis-Domain": isis}
                }
            ])
            break
        except ValueError:
            break
        except:
            continue

