import pynautobot
import pandas as pd



    
source = pd.ExcelFile('mastersheet_sharepoint_status_santized.xlsx')

site_df = pd.read_excel(source, 'DEVICE_INFORMATION')
nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")


for idx in range(0,len(site_df['hostname'])):

    name = site_df['hostname'][idx]
    isis = site_df['isis_all'][idx]
    print(name)

    
    try:
        nb.dcim.interfaces.create([
            {
                "device": {"name": name},
                "name" : 'Loopback0',
                "type" : 'virtual',
                "description": "default loopback",
                "custom_fields": {"Isis-Domain": isis}
            }
        ])
    except ValueError:
        continue

for idx in range(0,len(site_df['hostname'])):

    name = site_df['hostname'][idx]
    print(name)

    #nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")
    while True:
        try:
            nb.dcim.interfaces.create([
                {
                    "device": {"name": name},
                    "name" : 'Loopback1',
                    "type" : 'virtual',
                    "description": "network management loopback",
                    "custom_fields": {"VRF": "CIPR20000_TNTMGMT_H00"}
                }
            ])
            break
        except ValueError:
            break
        except:
            continue

for idx in range(0,len(site_df['hostname'])):

    name = site_df['hostname'][idx]
    print(name)
    isis = site_df['isis_all'][idx]

    anycast = site_df['lo100_ipv4'][idx]
    try:
        
        if '.' in anycast:
            #nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")

            while True:
                try:
                    nb.dcim.interfaces.create([
                        {
                            "device": {"name": name},
                            "name" : 'Loopback100',
                            "type" : 'virtual',
                            "description": "anycast loopback",
                            "custom_fields": {"Isis-Domain": isis}
                        }
                    ])
                    break
                except ValueError:
                    break
                except:
                    continue
        else:
            continue
    except:
        continue