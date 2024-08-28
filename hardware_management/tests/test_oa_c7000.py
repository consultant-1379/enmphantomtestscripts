import os

import pytest
import saninfo

@pytest.fixture
def my_fixture():
    ilo_host = "ieatlms3841ilo.athtem.eei.ericsson.se"
    ilo_username = 'root'
    ilo_password = 'shroot12'
    base_url = 'https://' + ilo_host
    server_url = 'https://ieatlms3841ilo.athtem.eei.ericsson.se/redfish/v1/systems/1'
    SYSTEM_URL = base_url
    LOGIN_ACCOUNT = ilo_username
    LOGIN_PASSWORD = ilo_password
    pass

def