import sys
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError
from get_resource_directory import get_resource_directory

def expand_data(_redfishobj, expand_url="/redfish/v1/"):
    exp_response = _redfishobj.get(expand_url+'?$expand=.')
    sys.stdout.write('\t'+str(exp_response.dict)+'\n')
    return (exp_response.dict)

def get_TLS_settings(_redfishobj):
    response = _redfishobj.get('/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/settings')
    print(response.dict)
    print(f' TLS ProtocolVersion : {response.dict["ProtocolVersion"]}')

def get_ciphers(_redfishobj):
    response = _redfishobj.get('/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/settings')
    #print(response.dict["Ciphers"])
    #response2 = _redfishobj.get('/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/baseconfigs')
    #baseconfig_ciphers = response2.dict["BaseConfigs"]
    #print(f'__TLS Ciphers in baseconfigs__ : {baseconfig_ciphers}')
    #print(f'__TLS Ciphers in settings : {baseconfig_ciphers}')
    return response.dict["Ciphers"]

def get_SecurityParams():
    SecurityParams = []
    data=expand_data(REDFISHOBJ, EXPAND_URL)
    count=data['Members@odata.count']
    print(count)
    for i in range(0, count):
        #expand_data(REDFISHOBJ, f'/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/{i}')
        response = REDFISHOBJ.get(f'/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/{i}')
        print(f'{response.dict["Name"]} : {response.dict["SecurityStatus"]} : {response.dict["State"]}')
        SecurityParams = SecurityParams + [{"Name" : response.dict["Name"], "SecurityStatus" : response.dict["SecurityStatus"] , "State": response.dict["State"]}]
    return SecurityParams

def get_security_params():
    for param in range(0, 11):
        y = redfish_obj.get(f"/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/{param}")
        for bit in y.dict:
            print(bit, ":", y.dict[bit])

if __name__ == "__main__":
    from definitions import SYSTEM_URL, LOGIN_ACCOUNT, LOGIN_PASSWORD

    # url to be expanded
    EXPAND_URL = "/redfish/v1/"
    EXPAND_URL = "/redfish/v1/JsonSchemas/Certificate/"
    EXPAND_URL = '/redfish/v1/SchemaStore/en/Certificate.json/'
    EXPAND_URL = '/redfish/v1/Systems/1/SmartStorage/ArrayControllers'
    EXPAND_URL = '/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/0'
    EXPAND_URL = '/redfish/v1/Systems/1'
    EXPAND_URL = '/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/'
    EXPAND_URL = '/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/baseconfigs'
    EXPAND_URL = '/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/settings'
    EXPAND_URL = '/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams'
    try:
        # Create a Redfish client object
        REDFISHOBJ = RedfishClient(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT, \
                                   password=LOGIN_PASSWORD)
        # Login with the Redfish client
        REDFISHOBJ.login()
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write(f"ERROR: server {SYSTEM_URL} not reachable or does not support RedFish.\n")
        sys.exit()
    # resource_instances = get_resource_directory(REDFISHOBJ)
    import pprint
    get_SecurityParams()
    get_security_params()

    print("\nCiphers : ",get_ciphers(REDFISHOBJ))
    get_TLS_settings(REDFISHOBJ)
    # for instance in resource_instances:
    #     sys.stdout.write(f"{instance['@odata.id']}\n")
    # for instance in resource_instances:
    #     # Use Resource directory to find the relevant URI
    #     sys.stdout.write(f"Use Resource directory to find the relevant URI {instance['@odata.id']}\n")
    #     expand_data(REDFISHOBJ, EXPAND_URL)
    REDFISHOBJ.logout()