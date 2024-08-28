import os,sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hwapp/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hwapp/logger')))

# Now you can import your module from the `src` directory



import hwapp.saninfo as saninfo

import hwapp.enminfo as enminfo
import hwapp.definitions as definitions


@pytest.fixture
def my_fixture():
    logname = definitions.LOG_ROOT + "pytest_test_saninfo.log"
    global logger
    logger = enminfo.activate_logging(logname)
    logger.info("pytest_my_fixture")
    hw_list = saninfo.getListofhardware("EMC VNX5400 DPE", dns_suffix=".athtem.eei.ericsson.se")
    return definitions.ROOT_DIR + os.sep
    # yield
    # logger.info("my_fixture teardown")


@pytest.fixture
def vnx_fixture():
    return enminfo.getListofhardware("EMC VNX5400 DPE", dns_suffix=".athtem.eei.ericsson.se")


# @pytest.mark.skip(reason="Test temporarily disabled")
def test_getVNXfirmware(my_fixture, caplog):
    assert 'enmphantomtestscripts\\hardware_management\\' in my_fixture
    # assert saninfo.activate_logging("log_saninfo.log")
    assert saninfo.getVNXfirmware("ieatvnx-77spa.athtem.eei.ericsson.se", "admin", "password") == "05.33.021.5.256"


# @pytest.mark.skip(reason="Test temporarily disabled")
def test_getUnityVersion():
    assert saninfo.getUnityVersion("ieatunityloaner327.athtem.eei.ericsson.se") == (
        '5.1.2', 'Unity 5.1.2.0 (Release, Build 007, 2021-12-22 13:10:36, 5.1.2.0.5.007)')
    assert saninfo.getUnityVersion("ieatunity-01.athtem.eei.ericsson.se") == ('5.0.2', None)


# @pytest.mark.skip(reason="Test temporarily disabled")
def test_main():
    assert saninfo.main("-s", "EMC UNITY 450F") == None
    assert saninfo.main("-s", "EMC VNX5400 DPE") == None


def test_get_ENMids_owning_vnx(my_fixture):
    hw_list = saninfo.getListofhardware("EMC VNX5400 DPE", dns_suffix=".athtem.eei.ericsson.se")
    enms = []
    for vnx in hw_list:
        enms.append(saninfo.get_ENMids_owning(vnx.split(".")[0].upper()))
    assert saninfo.get_ENMids_owning(vnx.split(".")[0].upper()) == ['ENM_5235_EEIDLE_D&S', 'ENM_5237_EEIDLE_D&S']


def test_get_ENMids_owning_unity(my_fixture):
    hw_list = saninfo.getListofhardware("EMC UNITY 450F", dns_suffix=".athtem.eei.ericsson.se")
    enms = []
    num_unitys = len(hw_list)
    assert num_unitys == 3
    for unity in hw_list:
        unity = unity.strip()
        enms.append(saninfo.get_ENMids_owning(unity.split(".")[0].upper()))
    assert enms == [['ENM_4416_EEICMUY_DDP_19.2-19.4'], ['ENM_5420_ETAMEHM_REM MTE_2019'], ['ENM_5596_EEIDLE_D&S']]


# @pytest.mark.xfail
def test_getListofhardware():
    assert saninfo.getListofhardware("EMC UNITY 450F", dns_suffix=".athtem.eei.ericsson.se") == \
           ['ieatunity-01.athtem.eei.ericsson.se', 'ieatunityloaner327.athtem.eei.ericsson.se',
            'ieatunity-12.athtem.eei.ericsson.se']
    assert saninfo.getListofhardware("EMC VNX5400 DPE", dns_suffix=".athtem.eei.ericsson.se") == [
        'ieatvnx-77.athtem.eei.ericsson.se', 'ieatvnx-102.athtem.eei.ericsson.se', 'ieatvnx-102.athtem.eei.ericsson.se']
