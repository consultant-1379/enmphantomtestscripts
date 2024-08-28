import redfish
#     jpayload = ''{
#   "ProtocolVersions": {
#     "TLS1_1": {
#       "Enabled": true
#     }
#   }
# }''
from redfish import RedfishClient
import requests,json,pprint
ilo_host = "ieatlms3841ilo.athtem.eei.ericsson.se"
ilo_host = "ieatvio025ilo.athtem.eei.ericsson.se"
# ilo_host = "ieatrcx8141lo.athtem.eei.ericsson.se"
ilo_host = "ieatrcx8045ilo.athtem.eei.ericsson.se"
ilo_username = 'root'
ilo_password = 'shroot12'
base_url = 'https://' + ilo_host
server_url = base_url + '/redfish/v1/systems/1'
SYSTEM_URL = base_url
LOGIN_ACCOUNT = ilo_username
LOGIN_PASSWORD = ilo_password
_redfishobj = RedfishClient(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT, \
                           password=LOGIN_PASSWORD)
_redfishobj.login()

response = _redfishobj.get('/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/settings')
print(response.dict["Ciphers"])
url = "https://{}/redfish/v1/SecurityService".format(ilo_host)
url = "https://{}/redfish/v1/".format(ilo_host)
url = base_url + "/redfish/v1/systems/1/bios/oem/hpe/tlsconfig/settings"
url = base_url + "/redfish/v1"
#url = "https://{}/redfish/v1/Systems/1".format(ilo_host)

# Set the authentication credentials
auth = (ilo_username, ilo_password)

# Set the request headers
headers = {"Content-Type": "application/json"}

# Send the GET request
response = requests.get(url, auth=auth, headers=headers, verify=False)

# Check the response status code
if response.status_code == 200:
    # Parse the response JSON data
    data = json.loads(response.text)
    print(data)
    tls_uri = data["Oem"]["Hpe"]['Links']['ResourceDirectory']['@odata.id']
    # pprint(_redfishobj.get_resource_directory())
    rd=_redfishobj.get_resource_directory()
    for x in rd:
        pprint(x)
    print(tls_uri)
    # print(data['TrustedModules'])
    # Retrieve the available protocol versions and their status
    protocol_version = data["ProtocolVersion"]
    print(protocol_version)
    tls_10_enabled = protocol_version["TLS1_0"]["Enabled"]
    print(tls_10_enabled)
    tls_11_enabled = protocol_versions["TLS1_1"]["Enabled"]
    tls_12_enabled = protocol_versions["TLS1_2"]["Enabled"]
    tls_13_enabled = protocol_versions.get("TLS1_3", {}).get("Enabled", False)

    # Print the results
    print("TLS 1.0 Enabled: {}".format(tls_10_enabled))
    print("TLS 1.1 Enabled: {}".format(tls_11_enabled))
    print("TLS 1.2 Enabled: {}".format(tls_12_enabled))
    print("TLS 1.3 Enabled: {}".format(tls_13_enabled))
else:
    print("Error: Unable to retrieve TLS settings (HTTP {} {})".format(response.status_code, response.reason))

