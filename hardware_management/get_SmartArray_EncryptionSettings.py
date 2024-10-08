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
An example of gathering the smart array encryption settings on HPE iLO systems
"""

import sys
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError

from get_resource_directory import get_resource_directory

def get_SmartArray_EncryptionSettings(_redfishobj, desired_properties):

    smartstorage_response = []
    smartarraycontrollers = dict()

    resource_instances = get_resource_directory(_redfishobj)
    if DISABLE_RESOURCE_DIR or not resource_instances:
        #if we do not have a resource directory or want to force it's non use to find the
        #relevant URI
        systems_uri = _redfishobj.root.obj['Systems']['@odata.id']
        systems_response = _redfishobj.get(systems_uri)
        systems_members_uri = next(iter(systems_response.obj['Members']))['@odata.id']
        systems_members_response = _redfishobj.get(systems_members_uri)
        smart_storage_uri = systems_members_response.obj.Oem.Hpe.Links\
                                                                ['SmartStorage']['@odata.id']
        smart_storage_arraycontrollers_uri = _redfishobj.get(smart_storage_uri).obj.Links\
                                                                ['ArrayControllers']['@odata.id']
        smartstorage_response = _redfishobj.get(smart_storage_arraycontrollers_uri).obj['Members']
    else:
        for instance in resource_instances:
            #Use Resource directory to find the relevant URI
            sys.stdout.write(f"Use Resource directory to find the relevant URI {instance['@odata.id']}\n")
            sys.stdout.write(f"@odata.type : {instance['@odata.type']}\n")

            if '#HpeSmartStorageArrayControllerCollection.' in instance['@odata.type']:
                smartstorage_uri = instance['@odata.id']
                print(f' smartstorage_uri {_redfishobj.get(smartstorage_uri)}')
                smartstorage_response = _redfishobj.get(smartstorage_uri).obj['Members']
                #smartstorage_response = _redfishobj.get(smartstorage_uri)
                sys.stdout.write(f"smartstorage_response : {smartstorage_response} Member.count= {_redfishobj.get(smartstorage_uri).obj['Members@odata.count']}\n")
                break

    for controller in smartstorage_response:
        smartarraycontrollers[controller['@odata.id']] = _redfishobj.get(controller['@odata.id']).\
                                                                                                obj
        sys.stdout.write("Encryption Properties for Smart Storage Array Controller \'%s\' : \n" \
                                        % smartarraycontrollers[controller['@odata.id']].get('Id'))
        for data in smartarraycontrollers[controller['@odata.id']]:
            if data in desired_properties:
                sys.stdout.write("\t %s : %s\n" % (data, smartarraycontrollers[controller\
                                                                        ['@odata.id']].get(data)))

def get_ciphers(_redfishobj):
        response = _redfishobj.get('/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/settings')
        print(response.dict["Ciphers"])
        response2 = _redfishobj.get('/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/baseconfigs')
        x = response2.dict["BaseConfigs"]
        print(f'__CIPHERS__ : {x}')
        return response.dict["Ciphers"]
if __name__ == "__main__":

    from definitions import SYSTEM_URL,LOGIN_ACCOUNT,LOGIN_PASSWORD

    #list of desired properties related to Smart Array controller encryption
    DESIRED_PROPERTIES = ["Name", "Model", "SerialNumber", "EncryptionBootPasswordSet",\
             "EncryptionCryptoOfficerPasswordSet",\
             "EncryptionLocalKeyCacheEnabled", "EncryptionMixedVolumesEnabled",\
             "EncryptionPhysicalDriveCount", "EncryptionRecoveryParamsSet",\
             "EncryptionStandaloneModeEnabled", "EncryptionUserPasswordSet"]
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

    get_SmartArray_EncryptionSettings(REDFISHOBJ, DESIRED_PROPERTIES)
    print("Ciphers : ",get_ciphers(REDFISHOBJ))
    REDFISHOBJ.logout()