import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hwapp/')))
import pytest

#import hwapp.saninfo as saninfo
import enminfo as  enminfo
import definitions as definitions


# @pytest.fixture
# def my_fixture():
#     logname = definitions.LOG_ROOT + "pytest_test_saninfo.log"
#     global logger
#     logger = enminfo.activate_logging(logname)
#     logger.info("pytest_my_fixture")
#     hw_list = saninfo.getListofhardware("EMC VNX5400 DPE", dns_suffix=".athtem.eei.ericsson.se")
#     return definitions.ROOT_DIR + os.sep
    # logger.info("my_fixture teardown")

# @pytest.fixture
# def vnx_fixture():
#     return enminfo.getListofhardware("EMC VNX5400 DPE", dns_suffix=".athtem.eei.ericsson.se")



def test_get_list_of_testplans():
    df = enminfo.get_eris_data_as_df()
    test_plan_list = enminfo.get_list_of_testplans(df,"PROLIANT DL3")
    print(test_plan_list)
    with open(definitions.LOG_ROOT + "test_get_list_of_testplans.log", 'w') as file:
        file.write( " ".join(test_plan_list))

    #assert test_plan_list.count() == 140
    # assert 'enmphantomtestscripts\\hardware_management\\' in my_fixture
    # # assert saninfo.activate_logging("log_saninfo.log")
    # assert saninfo.getVNXfirmware("ieatvnx-77spa.athtem.eei.ericsson.se", "admin", "password") == "05.33.021.5.256"