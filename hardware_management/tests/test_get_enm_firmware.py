import pandas as pd
from pandas.testing import assert_frame_equal

def test_dataframe_contains_expected_data():
    # Define the expected data
    expected_data = {
        'Testplan Name':['ENM_5600_EBHATAK_PLM_VIO_SIENM_M'],
        'CI Name': ['ieatvio023', 'ieatvio024', 'ieatvio025'],
        'Functional designation': ["HP PROLIANT DL380 GEN9", "HP PROLIANT DL380 GEN9", "HP PROLIANT DL380 GEN9"],
        'city': ['New York', 'Paris', 'London']
    }
    expected_data = {
        'Testplan Name': ['ENM_51078_EEIDLE_D&S'] ,
        'CI Name': ['ieatlms8148','ieatrcx8061','ieatrcx8067','ieatrcx8068'],
        'Functional designation': ['HPE PROLIANT DL360 GEN10 PLUS',
                                   'HPE PROLIANT DL360 GEN10 PLUS',
                                   'HPE PROLIANT DL360 GEN10 PLUS',
                                   'HPE PROLIANT DL360 GEN10 PLUS']
    }


    expected_df = pd.DataFrame(expected_data)

    # Create the actual DataFrame
    actual_data = {
        'name': ['John', 'Alice', 'Bob'],
        'age': [25, 30, 35],
        'city': ['New York', 'Paris', 'London']
    }
    actual_data = get_enm_hosts('ENM_51078_EEIDLE_D&S')
    actual_df = pd.DataFrame(actual_data)

    # Assert that the actual DataFrame is equal to the expected DataFrame
    assert_frame_equal(actual_df, expected_df)

import pytest
def test_get_enm_hosts():
    pass
    #assert get_enm_firmware.get_enm_hosts('ENM_5596_EEIDLE_D&S') == ['ieatlms7480',]
