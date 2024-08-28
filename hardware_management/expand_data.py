 # Copyright 2020 Hewlett Packard Enterprise Development LP
 #
 # Licensed under the Apache License, Version 2.0 (the "License"); you may
 # not use this file except in compliance with the License. You may obtain
 # a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 # License for the specific language governing permissions and limitations
 # under the License.

# -*- coding: utf-8 -*-
"""
An example of expanding data responses
"""

import sys
import json
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError
from get_resource_directory import get_resource_directory

def expand_data(_redfishobj, expand_url="/redfish/v1/"):

    response = _redfishobj.get(expand_url)
    exp_response = _redfishobj.get(expand_url+'?$expand=.')
    #sys.stdout.write('Standard response:\n')
    #sys.stdout.write('\t'+str(response.dict)+'\n')
    sys.stdout.write('Expanded response:\n')
    sys.stdout.write('\t'+str(exp_response.dict)+'\n')


if __name__ == "__main__":
    from definitions import SYSTEM_URL,LOGIN_ACCOUNT,LOGIN_PASSWORD

    #url to be expanded
    EXPAND_URL = "/redfish/v1/"
    EXPAND_URL = "/redfish/v1/JsonSchemas/Certificate/"
    EXPAND_URL = '/redfish/v1/SchemaStore/en/Certificate.json/'
    EXPAND_URL = '/redfish/v1/Systems/1/SmartStorage/ArrayControllers'
    EXPAND_URL = '/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/0'
    EXPAND_URL = '/redfish/v1/Systems/1'
    EXPAND_URL = '/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/'
    EXPAND_URL = '/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/baseconfigs'
    EXPAND_URL = '/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/settings'

    try:
        # Create a Redfish client object
        REDFISHOBJ = RedfishClient(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT, \
                                                                            password=LOGIN_PASSWORD)
        # Login with the Redfish client
        REDFISHOBJ.login()
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write(f"ERROR: server {SYSTEM_URL} not reachable or does not support RedFish.\n")
        sys.exit()
    resource_instances = get_resource_directory(REDFISHOBJ)
    expand_data(REDFISHOBJ, EXPAND_URL)
    for i in range(0,11):
        expand_data(REDFISHOBJ,f'/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/{i}')
        #expand_data(REDFISHOBJ,f'/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/{i}')
        pass
    for instance in resource_instances:
        sys.stdout.write(f"{instance['@odata.id']}\n")

    # for instance in resource_instances:
    #     # Use Resource directory to find the relevant URI
    #     sys.stdout.write(f"Use Resource directory to find the relevant URI {instance['@odata.id']}\n")
    #     expand_data(REDFISHOBJ, EXPAND_URL)
    REDFISHOBJ.logout()