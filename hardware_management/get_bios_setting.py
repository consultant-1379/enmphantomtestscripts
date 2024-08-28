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


import sys
import json
import argparse
from pprint import pprint
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError
import definitions
from enminfo import activate_logging

global DISABLE_RESOURCE_DIR


# from ilorest_util import get_resource_directory
# from ilorest_util import get_gen
def setup_logging(logfile):
    global logger
    logger = activate_logging(logfile)
    return logger


def get_bios_setting(_redfishobj):
    bios_uri = None
    bios_data = None
    resource_instances = _redfishobj.get_resource_directory()
    if DISABLE_RESOURCE_DIR or not resource_instances:
        # if we do not have a resource directory or want to force it's non use to find the
        # relevant URI
        systems_uri = _redfishobj.root.obj['Systems']['@odata.id']
        systems_response = _redfishobj.get(systems_uri)
        systems_members_uri = next(iter(systems_response.obj['Members']))['@odata.id']
        systems_members_response = _redfishobj.get(systems_members_uri)
        bios_uri = systems_members_response.obj['Bios']['@odata.id']
        bios_data = _redfishobj.get(bios_uri)
    else:
        # Use Resource directory to find the relevant URI
        for instance in resource_instances:
            if '#Bios.' in instance['@odata.type']:
                bios_uri = instance['@odata.id']
                bios_data = _redfishobj.get(bios_uri)
                break

    if bios_data:
        print("\n\nShowing bios attributes before changes:\n\n")
        print(json.dumps(bios_data.dict, indent=4, sort_keys=True))


def get_bios_setting_gen9(_redfishobj):
    bios_uri = "/redfish/v1/systems/1/bios"
    bios_data = None
    # Use Resource directory to find the relevant URI
    bios_data = _redfishobj.get(bios_uri)

    if bios_data:
        print("\n\nShowing bios attributes before changes:\n\n")
        print(json.dumps(bios_data.dict, indent=4, sort_keys=True))

def get_boot_options(_redfishobj, boot_options_url='/redfish/v1/Systems/1/BootOptions/'):
    data = _redfishobj.get(boot_options_url)
    count = data['Members@odata.count']
    for param in range(0, count):
        y = redfish_obj.get(f"{boot_options_url}{param}")
        for bit in y.dict:
            print(bit, ":", y.dict[bit])


def get_boot_settings():
    b = redfish_obj.get("/redfish/v1/systems/1/bios/oem/hpe/boot/settings")
    return (b)


if __name__ == "__main__":

    # SYSTEM_URL = input("Enter iLO IP Address: ")
    # LOGIN_ACCOUNT = input("Enter Username: ")
    # LOGIN_PASSWORD = input("Enter password: ")
    ilo_host = "ieatlms3841ilo.athtem.eei.ericsson.se"
    ilo_host = "ieatlms8147ilo.athtem.eei.ericsson.se"
    ilo_host = "ieatrcx8045ilo.athtem.eei.ericsson.se"
    ilo_username = 'root'
    ilo_password = 'shroot12'
    base_url = 'https://' + ilo_host
    server_url = 'https://ieatlms3841ilo.athtem.eei.ericsson.se/redfish/v1/systems/1'
    SYSTEM_URL = base_url
    LOGIN_ACCOUNT = ilo_username
    LOGIN_PASSWORD = ilo_password
    # logger = setup_logging(definitions.LOG_ROOT + "get_bios_settings.log")

    #     Initialize parser
    ##    parser = argparse.ArgumentParser(description = "Script to upload and flash NVMe FW")
    ##
    ##    parser.add_argument(
    ##        '-i',
    ##        '--ilo',
    ##        dest='ilo_ip',
    ##        action="store",
    ##        help="iLO IP of the server",
    ##        default=None)
    ##    parser.add_argument(
    ##        '-u',
    ##        '--user',
    ##        dest='ilo_user',
    ##        action="store",
    ##        help="iLO username to login",
    ##        default=None)
    ##    parser.add_argument(
    ##        '-p',
    ##        '--password',
    ##        dest='ilo_pass',
    ##        action="store",
    ##        help="iLO password to log in.",
    ##        default=None)
    ##
    ##    options = parser.parse_args()
    ##
    ##    system_url = "https://" + options.ilo_ip
    ##    print (system_url)

    DISABLE_RESOURCE_DIR = False

    try:
        # Create a Redfish client object
        # redfish_obj = RedfishClient(base_url=system_url, username=options.ilo_user, password=options.ilo_pass)
        redfish_obj = RedfishClient(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT, \
                                    password=LOGIN_PASSWORD)
        # Login with the Redfish client
        redfish_obj.login()
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or does not support RedFish.\n")
        sys.exit()
    (ilogen, _) = redfish_obj.get_gen()
    print("Generation is ", ilogen)
    if int(ilogen) == 5:
        # get_bios_setting(redfish_obj)
        # x=redfish_obj.get("/redfish/v1/systems/1/bios/oem")
        # x1=redfish_obj.get("/redfish/v1/systems/1/bios")
        # y=redfish_obj.get("/redfish/v1/chassis/1")
        # print(y.dict["Status"]["Health"])
        # y=redfish_obj.get("/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/2")
        # pprint(json.dumps(y.dict["Name"]))
        # print(y.dict["Name"])
        # y=redfish_obj.get("/redfish/v1/Managers/1/")
        # print(y.dict.keys())
        # print(y.dict["ManagerType"])
        # #print(y.dict["0"])
        # z=redfish_obj.get(("/redfish/v1/ResourceDirectory"))
        # pprint(json.dumps(z.dict))
        # print(y.dict["Status"]["Health"])
        # print(y.dict["@odata.id"])
        # print(y.dict["Status"]["Health"])
        get_boot_options(redfish_obj)
        pprint(get_boot_settings().dict)
        pprint(redfish_obj.get(f"/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/").dict)
        pprint(redfish_obj.get(f"/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/").dict[
                   'Members@odata.count'])
        # TODO
        '''
        BIOS Setting Fibre Channel/FCoE Scan Policy is set to Scan All Targets.

BIOS Setting Adapter Driver is enabled for all HBA card slots for Port 1.

BIOS Setting Selective Login is enabled for all HBA card slots for Port 1.

BIOS Setting Selective LUN Login is enabled for all HBA card slots for Port 1.

BIOS Setting World Login is disabled for all HBA card slots for Port 1.'''
    else:
        get_bios_setting_gen9(redfish_obj)
    redfish_obj.logout()
