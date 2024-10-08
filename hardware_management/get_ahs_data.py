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
An example of gathering AHS data for HPE iLO systems
"""

import sys
import json
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError

from hpeinfo import get_resource_directory

def get_ahs_data(_redfishobj, logfile):

    active_health_system_uri = None

    resource_instances = get_resource_directory(_redfishobj)
    if DISABLE_RESOURCE_DIR or not resource_instances:
        #if we do not have a resource directory or want to force it's non use to find the
        #relevant URI
        managers_uri = _redfishobj.root.obj['Managers']['@odata.id']
        managers_response = _redfishobj.get(managers_uri)
        managers_members_uri = next(iter(managers_response.obj['Members']))['@odata.id']
        managers_members_response = _redfishobj.get(managers_members_uri)
        active_health_system_uri = managers_members_response.obj.Oem.Hpe.Links\
                                    ['ActiveHealthSystem']['@odata.id']
    else:
        #Use Resource directory to find the relevant URI
        for instance in resource_instances:
            if '#HpeiLOActiveHealthSystem.' in instance['@odata.type']:
                active_health_system_uri = instance['@odata.id']

    if active_health_system_uri:
        active_health_system_response = _redfishobj.get(active_health_system_uri)
        active_health_system_log_uri = active_health_system_response.obj.Links['AHSLocation']\
                                                                                        ['extref']
        active_health_system_log_resp = _redfishobj.get(active_health_system_log_uri)
        if active_health_system_log_resp.status == 400:
            try:
                print(json.dumps(active_health_system_log_resp.obj['error']\
                                 ['@Message.ExtendedInfo'], indent=4, sort_keys=True))
            except Exception:
                sys.stderr.write("A response error occurred, unable to access iLO Extended "\
                                 "Message Info...")
        elif active_health_system_log_resp.status != 200:
            sys.stderr.write("An http response of \'%s\' was returned.\n" % active_health_system_log_resp.status)
        else:
            print("Success!\n")
            with open(logfile, 'wb') as ahsoutput:
                ahsoutput.write(active_health_system_log_resp.ori)
                ahsoutput.close()
                sys.stdout.write("AHS Data saved successfully as: \'%s\'" % logfile)

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
    ilo_host = "ieatlms3841ilo.athtem.eei.ericsson.se"
    ilo_username = 'root'
    ilo_password = 'shroot12'
    base_url = 'https://' + ilo_host
    server_url = 'https://ieatlms3841ilo.athtem.eei.ericsson.se/redfish/v1/systems/1'
    SYSTEM_URL = base_url
    LOGIN_ACCOUNT = ilo_username
    LOGIN_PASSWORD = ilo_password

    # logfile path and filename
    LOGFILE = "data.ahs"
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

    get_ahs_data(REDFISHOBJ, LOGFILE)
    REDFISHOBJ.logout()