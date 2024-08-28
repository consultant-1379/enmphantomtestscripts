from pprint import pprint
# import redfish
import json
import logging
from redfish import redfish_logger
import requests
# from urllib3.exceptions import InsecureRequestWarning
import sys
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError

import definitions

# # Suppress SSL certificate warnings

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# globals intended for HPE servers.
global SELECT
SELECT = "firmware"  # provide either 'software' or 'firmware' for inventory selection
global DISABLE_RESOURCE_DIR
DISABLE_RESOURCE_DIR = False


# flag to force disable resource directory. Resource directory and associated operations are

class ENM_ilohost:
    def __init__(self, ENM_booking,hostname, ilo_username=None, ilo_user_password=None):
        self.ENM_booking = ENM_booking
        self.ilo_host = hostname + "ilo.athtem.eei.ericsson.se"
        self.ilo_username = ilo_username
        self.ilo_user_password = ilo_user_password
        self.base_url = 'https://' + self.ilo_host
        self.server_url = self.base_url + '/redfish/v1/systems/1'
        self.bios_url = self.base_url + '/redfish/v1/systems/1/bios'
        self.NetworkInterfaces_url = self.base_url + '/redfish/v1/Systems/1/NetworkInterfaces'
        self.REDFISHOBJ = self.get_redfish_client()
        if self.REDFISHOBJ is not None:
            self.get_inventory_uri(self.REDFISHOBJ, SELECT)
        else:
            # write hostname/serialnumber and empty inventory values in CSV to indicate something is wrong
            HPE_server_firmware_csv = open(definitions.HPE_server_firmware_output, "a")
            sys.stderr.write("\tNo Refish object. Inventory empty.\n")
            HPE_server_firmware_csv.writelines(f'{self.ENM_booking}:{self.base_url.split("://")[1]}:::::::\n') # remove "https://"
            HPE_server_firmware_csv.close()
            #self.get_inventory(self.REDFISHOBJ, "")

    def close_session(self):
        self.REDFISHOBJ.logout()

    def get_redfish_client(self):
        try:
            self.logger.debug(f'get_redfish_client() :base_url =>{self.base_url}, before login')
            # Create a Redfish client object
            REDFISHOBJ = RedfishClient(base_url=self.base_url, username=self.ilo_username, \
                                       password=self.ilo_user_password)
            self.logger.debug(f'get_redfish_client() :base_url =>{self.base_url},still before login')

            # Login with the Redfish client
            REDFISHOBJ.login()
            self.logger.debug(f'get_redfish_client() :base_url =>{self.base_url}, after login')
        except ServerDownOrUnreachableError as excp:
            sys.stderr.write(f"ERROR: server {self.base_url} not reachable or does not support RedFish.\n {excp}")
            self.close_session()
            sys.exit()
        except Exception as e:
            sys.stderr.write(f"ERROR: server ## {self.base_url} ## not reachable or does not support RedFish.\n {e}")
            REDFISHOBJ = None
        return (REDFISHOBJ)

    def set_admin_user(self, ilo_username):
        self.ilo_username = ilo_username

    def get_admin_user(self):
        return self.ilo_username

    def set_admin_user_password(self, ilo_user_password):
        self.ilo_user_password = ilo_user_password

    def get_admin_user_password(self):
        return self.ilo_user_password

    def __str__(self):
        return ('<%s => %s: hostname>' %
                (self.__class__.__name__, self.ilo_host))

    LOGGERFILE = definitions.LOG_ROOT + "RedfishApi.log"
    print(LOGGERFILE)
    LOGGERFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logger = redfish_logger(LOGGERFILE, LOGGERFORMAT, logging.WARNING)
    # logger = redfish_logger("logs" + os.sep + LOGGERFILE, LOGGERFORMAT, logging.WARNING)

    # intended for HPE servers.

    def get_response(self, url):
        ilo_firmare_version = ""
        response = requests.get(url, headers=headers, auth=(self.ilo_username, self.ilo_host), verify=False)
        return response

    def get_bios_version(self, firmware_inventory):
        BiosVersion = requests.get(self.bios_url, headers=headers, auth=(self.ilo_username, self.ilo_user_password),
                                   verify=False)
        pprint(f"BiosVersion = {firmware_inventory['BiosVersion']}")
        self.logger.debug(f'{BiosVersion}')
        return BiosVersion

    def get_resource_directory(self, redfishobj):
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

    def get_gen(self, _redfishobj):
        rootresp = _redfishobj.root.obj
        # Default iLO 5
        ilogen = 5
        gencompany = next(iter(rootresp.get("Oem", {}).keys()), None) in ('Hpe', 'Hp')
        comp = 'Hp' if gencompany else None
        comp = 'Hpe' if rootresp.get("Oem", {}).get('Hpe', None) else comp
        if comp and next(iter(rootresp.get("Oem", {}).get(comp, {}).get("Manager", {}))). \
                get('ManagerType', None):
            ilogen = next(iter(rootresp.get("Oem", {}).get(comp, {}).get("Manager", {}))) \
                .get("ManagerType")
            ilover = next(iter(rootresp.get("Oem", {}).get(comp, {}).get("Manager", {}))). \
                get("ManagerFirmwareVersion")
            if ilogen.split(' ')[-1] == "CM":
                # Assume iLO 4 types in Moonshot
                ilogen = 4
                iloversion = None
            else:
                ilogen = ilogen.split(' ')[1]
                iloversion = float(ilogen.split(' ')[-1] + '.' + \
                                   ''.join(ilover.split('.')))
        self.logger.debug(f'iloversion : {iloversion}')

        return (ilogen, iloversion)

    def get_inventory_uri(self, _redfishobj, select):
        update_service_uri = None
        inventory_uri = None

        resource_instances = self.get_resource_directory(_redfishobj)
        if DISABLE_RESOURCE_DIR or not resource_instances:
            # if we do not have a resource directory or want to force it's non use to find the
            # relevant URI
            self.logger.debug(f'get_inventory_uri() :DISABLE_RESOURCE_DIR =>{DISABLE_RESOURCE_DIR}, resource_instances =>{resource_instances}')
            try:
                update_service_uri = _redfishobj.root.obj['UpdateService']['@odata.id']
            except KeyError:
                sys.stderr.write(f"Workaround - Skipping {self.serial_number()}  .\n")
        else:
            # Use Resource directory to find the relevant URI
            for instance in resource_instances:
                if '#UpdateService.' in instance['@odata.type']:
                    update_service_uri = instance['@odata.id']
        self.logger.debug(f'update_service_uri :{update_service_uri}')

        if update_service_uri:
            update_service_resp = _redfishobj.get(update_service_uri)
            self.logger.debug(f'select :{select}')
            if "software" in select.lower():
                inventory_uri = update_service_resp.obj['SoftwareInventory']['@odata.id']
            elif "firmware" in select.lower():
                inventory_uri = update_service_resp.obj['FirmwareInventory']['@odata.id']
            else:
                raise Exception("Invalid selection provided: Please select 'software' or 'firmware' " \
                                "to obtain the relevant inventory data.")
            sys.stdout.write("Printing data in inventory: %s\n" % inventory_uri)
            self.get_inventory(_redfishobj, inventory_uri)

    def get_inventory(self, _redfishobj, inventory_uri):
        # Write inventory to csv file
        HPE_server_firmware_csv = open(definitions.HPE_server_firmware_output, "a")
        # if _redfishobj is None:
        #     sys.stderr.write("\tNo Refish object. Inventory empty.\n")
        #     HPE_server_firmware_csv.writelines(f'{self.base_url}::::::\n')
        _members = _redfishobj.get(inventory_uri).obj['Members']
        if not _members:
            sys.stderr.write("\tInventory empty.\n")
            HPE_server_firmware_csv.writelines(f'{self.ENM_booking}:{self.base_url.split("://")[1]}:::::::\n') # remove "https://"
        else:
            HPE_server_firmware_csv = open(definitions.HPE_server_firmware_output, "a")
            response = _redfishobj.get('/redfish/v1/systems/1')

            for inventory_item in _members:
                _resp = _redfishobj.get(inventory_item['@odata.id'])
                sys.stdout.write(f'{self.ENM_booking}:{response.dict["HostName"]}:{response.dict["SerialNumber"]}:{response.dict["Model"]}:{_resp.dict.get("Name")}: {_resp.dict.get("Description")}: {_resp.dict.get("Id")}:{_resp.dict.get("Version")}:\n')
                HPE_server_firmware_csv.writelines(f'{self.ENM_booking}:{response.dict["HostName"]}:{response.dict["SerialNumber"]}:{response.dict["Model"]}:{_resp.dict.get("Name")}: {_resp.dict.get("Description")}: {_resp.dict.get("Id")}:{_resp.dict.get("Version")}:\n')
                # TODO print(json.dumps(_resp.dict, indent=4, sort_keys=True))
        HPE_server_firmware_csv.close()

    def computer_details(self):
        _redfishobj = self.REDFISHOBJ
        systems_members_uri = None
        systems_members_response = None

        resource_instances = self.get_resource_directory(_redfishobj)
        if DISABLE_RESOURCE_DIR or not resource_instances:
            # if we do not have a resource directory or want to force it's non use to find the
            # relevant URI
            systems_uri = _redfishobj.root.obj['Systems']['@odata.id']
            systems_response = _redfishobj.get(systems_uri)
            systems_members_uri = next(iter(systems_response.obj['Members']))['@odata.id']
            systems_members_response = _redfishobj.get(systems_members_uri)
        else:
            for instance in resource_instances:
                # Use Resource directory to find the relevant URI
                if '#ComputerSystem.' in instance['@odata.type']:
                    systems_members_uri = instance['@odata.id']
                    systems_members_response = _redfishobj.get(systems_members_uri)

        print("\n\nPrinting computer system details:\n\n")
        print(json.dumps(systems_members_response.dict, indent=4, sort_keys=True))

    def get_TotalSystemMemoryGiB(self):
        _redfishobj = self.REDFISHOBJ
        systems_members_uri = None
        systems_members_response = None

        resource_instances = self.get_resource_directory(_redfishobj)
        if DISABLE_RESOURCE_DIR or not resource_instances:
            # if we do not have a resource directory or want to force it's non use to find the
            # relevant URI
            systems_uri = _redfishobj.root.obj['Systems']['@odata.id']
            systems_response = _redfishobj.get(systems_uri)
            systems_members_uri = next(iter(systems_response.obj['Members']))['@odata.id']
            systems_members_response = _redfishobj.get(systems_members_uri)
        else:
            for instance in resource_instances:
                # Use Resource directory to find the relevant URI
                print(instance['@odata.type'])
                if '#ComputerSystem.' in instance['@odata.type']:
                    systems_members_uri = instance['@odata.id']
                    systems_members_response = _redfishobj.get(systems_members_uri)

        print("\n\nPrinting computer system details:\n\n")
        #print(json.dumps(systems_members_response.dict, indent=4, sort_keys=True))
        print('TotalSystemMemoryGiB : ',systems_members_response.dict['MemorySummary']['TotalSystemMemoryGiB'])
        print('ProcessorSummary : ', systems_members_response.dict['ProcessorSummary'])
        print(' : ', systems_members_response.dict)

    def get_TlsConfig(self):
        _redfishobj = self.REDFISHOBJ
        systems_members_uri = None
        systems_members_response = None
        resource_instances = self.get_resource_directory(_redfishobj)
        if DISABLE_RESOURCE_DIR or not resource_instances:
            # if we do not have a resource directory or want to force it's non use to find the
            # relevant URI
            systems_uri = _redfishobj.root.obj['Systems']['@odata.id']
            systems_response = _redfishobj.get(systems_uri)
            systems_members_uri = next(iter(systems_response.obj['Members']))['@odata.id']
            systems_members_response = _redfishobj.get(systems_members_uri)
        else:
            for instance in resource_instances:
                # Use Resource directory to find the relevant URI
                print(instance['@odata.type'])
                if '#HpeTlsConfig.' in instance['@odata.type']:
                    systems_members_uri = instance['@odata.id']
                    systems_members_response = _redfishobj.get(systems_members_uri)

        print("\n\nPrinting TLS  details:\n\n")
        print('TLS ProtocolVersion : ', systems_members_response.dict['ProtocolVersion'])
        print(' : ', systems_members_response.dict)
        print(_redfishobj.get(systems_members_response.dict['@odata.id']))

    def hardware_model(self):
        Hardware_Model = None
        client = self.get_redfish_client()
        response = client.get('/redfish/v1/systems/1')
        Hardware_Model = response.dict["Model"]
        print(response.dict["Model"])
        return Hardware_Model
    def serial_number(self):
        serial_number = None
        client = self.get_redfish_client()
        response = client.get('/redfish/v1/systems/1')
        print(response.dict.keys())
        # for key in response.dict.keys():
        #     print(f'{key} : {response.dict[key]}')
        print(response.dict["HostName"])
        print(response.dict["SerialNumber"])
        serial_number = response.dict["SerialNumber"]
        print(response.dict["Model"])
        return serial_number

if __name__ == "__main__":


    # Create a Redfish client object
    #enm = ENM_ilohost("ieatlms3841", "root", "shroot12")
    #enm = ENM_ilohost("ieatombs5506", "root", "shroot12")
    enm = ENM_ilohost("ENM_51071_EEIDLE_D&S","ieatrcx8045", "root", "shroot12")


    if enm.REDFISHOBJ is not None:
        system_data = enm.REDFISHOBJ.get("/redfish/v1/systems/1")
        #enm.logger.info(system_data)
        # enm.computer_details()
        #enm.serial_number()
        enm.computer_details()
        #enm.get_TotalSystemMemoryGiB()
        enm.get_TlsConfig()
        enm.close_session()
    print("============== hpilo =============")

    # pprint(f'get_gen = {get_gen(REDFISHOBJ)}')
    print("===============end get_gen ==========")
    # # TODO pprint(f'get_resources = {get_resource_directory(REDFISHOBJ)}')
    # Set up the request headers
    headers = {'Accept': 'application/json'}
    # # Make the HTTP GET request
    # response = requests.get(enm.server_url, headers=headers, auth=(enm.ilo_username, enm.ilo_user_password),
    #                         verify=False)
    # # Check the response status code
    # if response.status_code == 200:
    #     # Parse the JSON response
    #     firmware_inventory = response.json()
    #     # TODO pprint(firmware_inventory)
    #     pprint(firmware_inventory.keys())
    #     # TODO pprint(f' oem = {firmware_inventory["Oem"]["Hpe"].keys()}')
    #
    #     # pprint(f"NetworkInterfaces_url = {get_response(NetworkInterfaces_url).json()['Members']}")
    #     # pprint(f"NetworkInterfaces_url__ = {get_response(nic1_url).json().keys()}")
    #     # pprint(f"NetworkInterfaces_url__ = {get_response(nic1_url).json()}")
    #
    #     EthernetInterfaces = firmware_inventory['EthernetInterfaces']
    #     pprint(f'EthernetInterfaces = {EthernetInterfaces}')
    #     pprint("===============  firmware_version ============")
    #     pprint(f"Bios = {firmware_inventory['Bios']}")
    #     enm.get_bios_version(firmware_inventory)
    #     pprint(f'IntelligentProvisioningVersion = {firmware_inventory["Oem"]["Hpe"]["IntelligentProvisioningVersion"]}')
    #     print("=============== Other useful stuff =================")
    #     SerialNumber = firmware_inventory['SerialNumber']
    #     pprint(f'SerialNumber = {SerialNumber}')
    #
    #     # Print firmware information
    #     # for firmware in firmware_inventory['Managers']:
    #     #     print(firmware['@odata.id'], firmware['BiosVersion'])
    # else:
    #     print('Error: Failed to retrieve firmware information.')

