import pynautobot
import pandas as pd



    
source = pd.ExcelFile('mastersheet_sharepoint_status_santized.xlsx')

site_df = pd.read_excel(source, 'DEVICE_INFORMATION')
nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/devices/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

#len(site_df['hostname'])

for idx in range(0,len(site_df['hostname'])):
    site = site_df['site'][idx]
    name = site_df['hostname'][idx]
    print(name)
    device_role = site_df['device_role'][idx]
    print(device_role)
    device_type = site_df['device_type'][idx]
    print(device_type)
    region = site_df['region'][idx]
    rfs = site_df['rfs'][idx]

    
    
    pfx = int(site_df['lo0_sid'][idx])

    idxx = int(pfx) - 16000

    try:
        any = int(site_df['lo100_sid'][idx])

        
        
        try:
            nb.dcim.devices.create([
                {
                    "name": name,
                    "device_role": {"name":device_role},
                    "device_type" : {"model":device_type},
                    "region": {"name":region},
                    "site":{"name":site},
                    "status":rfs,
                    "custom_fields": {"Anycast-Sid": any,"Index": idxx,"Network": "Cisco TNT","Phase": "LOT23 PHASE 1","Prefix-Sid": pfx},

                }
            ])
        except ValueError:
            continue
    except ValueError:
        
        try:
            nb.dcim.devices.create([
                {
                    "name": name,
                    "device_role": {"name":device_role},
                    "device_type" : {"model":device_type},
                    "region": {"name":region},
                    "site":{"name":site},
                    "status":rfs,
                    "custom_fields": {"Index": idxx,"Network": "Cisco TNT","Phase": "LOT23 PHASE 1","Prefix-Sid": pfx},

                }
            ])
        except ValueError:
            continue