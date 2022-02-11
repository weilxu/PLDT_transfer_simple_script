import pynautobot
import pandas as pd



    
source = pd.ExcelFile('mastersheet_sharepoint_status_santized.xlsx')

site_df = pd.read_excel(source, 'SITES')

#len(site_df['hostname']


for idx in range(0,len(site_df['hostname'])):
    site = site_df['site'][idx]
    print(site)
    slug = ('-').join(site.lower().split(' '))
    name = site_df['hostname'][idx]
    region = site_df['region'][idx]
    address = site_df['snmp_location'][idx]

    nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/sites/?", token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")
    try:

        nb.dcim.sites.create([
            {
                "name": site,
                "slug": slug,
                "status": "Active",
                "region": {"name":region},
                "physical_address": address,
                "custom_fields": {"Area": "AREA 1","Network": "Cisco TNT" }
            }
        ])

    except ValueError:
        continue