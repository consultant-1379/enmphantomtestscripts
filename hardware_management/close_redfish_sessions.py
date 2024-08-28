import requests
import json

# specify the endpoint URL for Redfish sessions
url = "https://ieatrcx8141ilo.athtem.eei.ericsson.se/redfish/v1/SessionService/Sessions"

# specify the headers for the request
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# make the GET request to retrieve the sessions
response = requests.get(url, headers=headers, verify=False)

# parse the JSON response to get the session IDs
data = json.loads(response.text)
sessions = data["Members"]
session_ids = [session["@odata.id"].split("/")[-1] for session in sessions]
print(sessions)
print(session_ids)
# # close the session with a specific session ID
# session_id_to_close = "session-id-to-close"
# url_to_close = url + "/" + session_id_to_close
# response = requests.delete(url_to_close, headers=headers, verify=False)
#
# if response.status_code == 204:
#     print(f"Session {session_id_to_close} has been closed successfully.")
# else:
#     print(f"Failed to close session {session_id_to_close}.")


