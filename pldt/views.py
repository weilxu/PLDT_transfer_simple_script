import pynautobot
import pandas as pd
from django.shortcuts import render
import requests


def home(request):
    source = pd.ExcelFile('C:\\Users\\weilxu\\PycharmProjects\\PLDTtest\\upload\\PLDT_v5.xlsx')

    site_df = pd.read_excel(source, 'Sheet')

    # # len(site_df['hostname']
    #
    for idx in range(0, len(site_df['Device Names'])):
        name = site_df['Device Names'][idx]
        address = site_df['IP Address'][idx]+site_df['Subnet'][idx]
        type = site_df['Device Types'][idx]
        name_i = ''
        type_i = ''
        mgmt = ''
        if type == 'Cisco NCS 2006':
            name_i = 'CTC'
            type_i = 'virtual'
            mgmt = 'false'
        elif type == 'Cisco NCS 4016':
            name_i = 'MgmtEth0/RP0/CPU0/0'
            type_i = '1000base-t'
            mgmt = 'false'
        elif type == 'Cisco NCS 1004':
            name_i = 'MgmtEth0/RP0/CPU0/0'
            type_i = '1000base-t'
            mgmt = 'true'
        elif type == 'Cisco Catalyst 36xx':
            name_i = 'Gi1/1/4'
            type_i = '1000base-t'
            mgmt = 'false'
        # site = site_df['Site Names'][idx]
        # site_u = site.upper()
        # slug = (('-').join(site.lower().split(' '))).replace('.', '')
        # name = site_df['Region'][idx]
        # region = site_df['Device Type'][idx]
        # address = site_df['IP Address'][idx]
        headers = {
            'Authorization': 'Token b7d568b9a5a400a249a057fca8a2b0d6dcc05828',
            'Content-Type': 'application/json',
            'Accept': 'application/json; indent=4',
        }
    # while True:
    # try:
    #     response = requests.get(
    #         f'http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?device={name}',
    #         headers=headers)
    #
    #     parse = response.json()
    #     x = parse['results']
    #     y = x[0]['id']
    # except ValueError:
    #     print('erro')

        # for x in parse['results']:
        #     id = 0
        #
        #     id = x['id']
        #     print(id)

        nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/ipam/ip-addresses/?",
                        token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")
        try:
            response = requests.get(
                f'http://pldt-tnt-inventory.cisco.com/api/dcim/interfaces/?device={name}',
                headers=headers)

            parse = response.json()
            x = parse['results']
            y = x[0]['id']
            nb.ipam.ip_addresses.create([

                {

                    "family": {
                        "value": 4,
                        "label": "IPv4"
                    },
                    "address": address,
                    "status": "In-use",
                    "assigned_object_type": "dcim.interface",
                    "assigned_object_id": y,
                    "assigned_object": {
                        "device": {
                            "name": name,
                            "display_name": name
                        },
                        "name": name_i,
                    },
                    "description": "up720"
            }

        ])
        #     nb.dcim.interfaces.create([
        #         {
        #             "device": {"name": name},
        #             "name": name_i,
        #             "type": type_i,
        #             "mgmt_only": mgmt
        #         }
        #     ])

    #         nb.dcim.devices.create([
    #             {
    #                 "name": name,
    #                 "device_role": {"name": role},
    #                 "device_type": {"model": type},
    #                 "site": {"name": site_u},
    #                 "status": 'RFS',
    #                 "tags": [
    #                     {
    #                         "name": "PHASE 1",
    #                         "slug": "phase-1",
    #                     }
    #                 ],
    #                 "comments": "up720",
    #                 "custom_fields": {"Network": "Cisco TNT", "Phase": "LOT 1 PHASE 1"},
    #
    #             }
    #         ])
        except ValueError:
            # return render(request, 'erro.html')
            continue
    return render(request, 'success.html')
    #
    #     nb = pynautobot.api("http://pldt-tnt-inventory.cisco.com/api/dcim/sites/?",
    #                     token="b7d568b9a5a400a249a057fca8a2b0d6dcc05828")
    #     try:
    #     # print(site,slug,name,region,address)
    #         nb.dcim.sites.create([
    #             {
    #                 "name": site,
    #                 "slug": slug,
    #                 "status": "Active",
    #                 "region": {"name": name},
    #                 "description": "up716",
    #                 "physical_address": address,
    #                 "custom_fields": {"Area": "AREA 1", "Network": "Cisco TNT"},
    #
    #             }
    #         ])
    #
    #     except ValueError:
    #         continue


# Create your views here.
