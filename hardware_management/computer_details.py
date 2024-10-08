

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
An example of gathering the computer system details
"""


import sys
import json
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError


def get_resource_directory( redfishobj):
     try:
         resource_uri = redfishobj.root.obj.Oem.Hpe.Links.ResourceDirectory['@odata.id']
     except KeyError:
         sys.stderr.write("Resource directory is only available on HPE servers.\n")
         return None

     response = redfishobj.get(resource_uri)
     resources = []

     if response.status == 200:
         sys.stdout.write("\tFound resource directory at /redfish/v1/resourcedirectory" + "\n\n")
         resources = response.dict["Instances"]
     else:
         sys.stderr.write("\tResource directory missing at /redfish/v1/resourcedirectory" + "\n")

     return resources

def computer_details(_redfishobj):
    systems_members_uri = None
    systems_members_response = None

    resource_instances = get_resource_directory(_redfishobj)
    if DISABLE_RESOURCE_DIR or not resource_instances:
        #if we do not have a resource directory or want to force it's non use to find the
        #relevant URI
        systems_uri = _redfishobj.root.obj['Systems']['@odata.id']
        systems_response = _redfishobj.get(systems_uri)
        systems_members_uri = next(iter(systems_response.obj['Members']))['@odata.id']
        systems_members_response = _redfishobj.get(systems_members_uri)
    else:
        for instance in resource_instances:
            #Use Resource directory to find the relevant URI
            if '#ComputerSystem.' in instance['@odata.type']:
                systems_members_uri = instance['@odata.id']
                systems_members_response = _redfishobj.get(systems_members_uri)

    print("\n\nPrinting computer system details:\n\n")
    print(json.dumps(systems_members_response.dict, indent=4, sort_keys=True))

if __name__ == "__main__":
    # When running on the server locally use the following commented values
    #SYSTEM_URL = None
    #LOGIN_ACCOUNT = None
    #LOGIN_PASSWORD = None

    # When running remotely connect using the secured (https://) address,
    # account name, and password to send https requests
    # SYSTEM_URL acceptable examples:
    # "https://10.0.0.100"
    # "https://ilo.hostname"
    # Set up iLO credentials and server URL
    ilo_host = "ieatlms3841ilo.athtem.eei.ericsson.se"
    ilo_host = "ieatvio025ilo.athtem.eei.ericsson.se"
    # ilo_host = "ieatrcx8141lo.athtem.eei.ericsson.se"
    ilo_username = 'root'
    ilo_password = 'shroot12'
    base_url = 'https://' + ilo_host
    server_url = base_url + '/redfish/v1/systems/1'
    SYSTEM_URL = base_url
    LOGIN_ACCOUNT = ilo_username
    LOGIN_PASSWORD = ilo_password

    # flag to force disable resource directory. Resource directory and associated operations are
    # intended for HPE servers.
    DISABLE_RESOURCE_DIR = False

    try:
        # Create a Redfish client object
        REDFISHOBJ = RedfishClient(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT, \
                                                                            password=LOGIN_PASSWORD)
        # Login with the Redfish client
        REDFISHOBJ.login()
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or does not support RedFish.\n")
        sys.exit()

    computer_details(REDFISHOBJ)
    REDFISHOBJ.logout()
