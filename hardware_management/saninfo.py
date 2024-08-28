# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import jinja2
# requires requests, pandas, openpyxl, redfish
import os
import re
import sys
import enminfo
import requests
import json
import pandas as pd
import platform  # For getting the operating system name
import subprocess  # For executing a shell command
import inspect
import logging
from definitions import DATA_PATH
from enminfo import get_eris_file, get_ENMids_owning,activate_logging,getListofhardware

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
if not opts:
    opts = "-v"
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

global logger
logger = enminfo.activate_logging()
# eris_file = DATA_PATH + "eris_export_ENM_200123.xlsx"
eris_file = DATA_PATH + "eris_export_ENM_test.xlsx"
sheet = "Sheet1"

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    logger.debug(f"subrocess.run command is :{str(command)}")
    p = subprocess.run(command, stdout=subprocess.DEVNULL)  # capture_output=True,check=True)
    # p = subprocess.Popen(command,shell=False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).wait()
    return p.returncode == 0


def getUnitySoftwareVersion(json_response):
    oeversion = ""
    oe_fullversion = None
    for k in json_response:
        if k == "entries":
            entrieslist = json_response[k]
            entriesdict = entrieslist[0]
            for k2 in entriesdict:
                # logger.info("key2 :", k2, "val2", entriesdict[k2])
                for k3 in entriesdict['content']:
                    # logger.info("key3 :", k3, "val3", entriesdict['content'][k3])
                    if k3 == "softwareFullVersion":
                        oe_fullversion = entriesdict['content'][k3]
                    if k3 == "softwareVersion":
                        oeversion = entriesdict['content'][k3]
                return oeversion, oe_fullversion


def getUnityVersion(unityurl):
    my_headers = {'Accept': 'application/json', 'Content-type': 'application/json', 'X-EMC-REST-CLIENT': 'true'}
    url_basicSystemInfo = "https://" + unityurl + "/api/types/basicSystemInfo/instances"
    url_basic_01 = "https://ieatunity-01.athtem.eei.ericsson.se/api/types/basicSystemInfo/instances"
    js327 = {
        "@base": "https://ieatunityloaner327.athtem.eei.ericsson.se/api/types/basicSystemInfo/instances?per_page=2000",
        "updated": "2023-01-22T17:24:34.944Z", "links": [{"rel": "self", "href": "&page=1"}], "entries": [
            {"@base": "https://ieatunityloaner327.athtem.eei.ericsson.se/api/instances/basicSystemInfo",
             "updated": "2023-01-22T17:24:34.944Z", "links": [{"rel": "self", "href": "/0"}],
             "content": {"id": "0", "model": "Unity 450F", "name": "ieatunityloaner327", "softwareVersion": "5.1.2",
                         "softwareFullVersion": "Unity 5.1.2.0 (Release, Build 007, 2021-12-22 13:10:36, 5.1.2.0.5.007)",
                         "apiVersion": "11.0", "earliestApiVersion": "4.0"}}]}
    try:
        requests.packages.urllib3.disable_warnings()

        # r = requests.get(url_basic_327,auth=('admin','Password123#'))
        r = requests.get(url_basicSystemInfo, headers=my_headers,
                         verify=False, timeout=3.5)
        json_response = json.loads(r.text)
    except Exception as e:
        logger.info('Request has timed out')
        logger.exception(f'caught {type(e)}: {e}')
        logger.error(f"json_response = json.loads({r.text})")

        return ("Not Found", "Not Found")
    return (getUnitySoftwareVersion(json_response))





def getUnitylist(hardwaremodel):
    logger.info("getUnitylist")
    #print(f"printing in getUnityList hardwaremodel is : {hardwaremodel}")
    logger.debug(f"getUnitylist: {hardwaremodel}")
    hw_list = getListofhardware(hardwaremodel, dns_suffix=".athtem.eei.ericsson.se")
    # logger.debug(f"hw_list: {hw_list}")
    # logger.info("DEBUG: cwd for function: " + inspect.currentframe().f_code.co_name, os.getcwd())
    unityfirmare_log = open("unityfirmware.log", "w")
    for line in hw_list:
        enm_id = get_ENMids_owning(line.strip().split(".")[0].upper())    # remove dns suffix
        logger.info(f"{enm_id}")
        if ping(line.strip()):
            pingresult = f'{line.strip()} \t Ping SUCCESS \t '
            # logger.info(pingresult, end="\t")
            oeversion, oefullversion = getUnityVersion(line.strip())
            logger.info(f"{enm_id}, {pingresult}    Unity OE Version :   {oeversion} Full Version : {oefullversion}")
            # res = enm_id + " :\t" + pingresult + "\t" + "Unity OE Version :" + str(oeversion) + "Full Version :" + str(
            #     oefullversion)
            res = f'{enm_id}\t{pingresult}\t{str(oeversion)}\t{str(oefullversion)}\r'
            yield res
        else:
            pingresult = f'{enm_id} :{line.strip()} \t Ping FAILED '
            logger.info(pingresult)
            yield pingresult + " Ping FAILED"

        try:
            unityfirmare_log.writelines(res)
        except Exception as e:
            logger.critical(f'caught {type(e)}: {e}')
    unityfirmare_log.close()
    return


def getVNXfirmware(fqdn, user, password):
    # /opt/Navisphere/bin/naviseccli -User admin -Password password -Scope global -Address ieatvnx-151spa.athtem.eei.ericsson.se getagent | grep "Revision:"
    # Revision:            05.33.021.5.256
    cmd = 'c:\\Program Files (x86)\\EMC\\Navisphere CLI\\NaviSECCli.exe' if platform.system().lower() == 'windows' \
        else '/opt/Navisphere/bin/naviseccli'
    command = [cmd, "-User", user, "-Password",
               password, "-Scope", "global", "-Address",
               fqdn, "getagent", "-rev"]
    try:
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate(input=b'1\n')
        prompt_output = output.decode('utf-8')
        # print("prompt_output =",prompt_output)
        pattern = (r'.*Revision:')
        match = re.search(pattern, prompt_output)
        if match:
            # print("Match found!")
            end_index = match.end()
            oe_firmware_revision = str(prompt_output[end_index:]).strip()
            # print("oe firmware revision =",oe_firmware_revision)

        else:
            print("Match not found in :", prompt_output)
            oe_firmware_revision = ""
        logger.info(f'oe_firmware_revision={oe_firmware_revision}')
        # output = subprocess.Popen(command).communicate()[0]
        return oe_firmware_revision
    except(FileNotFoundError):
        logger.info(f"ERROR FileNotFoundError : {command} " + inspect.currentframe().f_code.co_name, os.getcwd())
        raise


def getVNXlist(hardwaremodel):
    hw_list = getListofhardware(hardwaremodel, dns_suffix="spa.athtem.eei.ericsson.se")
    vnxfirmare_log = open("vnxfirmware.log", "w")
    logger.debug(f"getVNXlist hw_list = {hw_list}")
    #print(f'getVNXlist hw_list = {hw_list}')
    for vnx in hw_list:
        logger.info(f"line= {vnx}")
        print(f'vnx={vnx}')
        enm_id = get_ENMids_owning(vnx.strip().split("spa.")[0].upper())
        logger.info(f"enm_id= {enm_id}")
        if ping(vnx.strip()):
            logger.info(f"{vnx.strip()} \t===>Ping Success" )
            pingresult = f'{vnx.strip()} \t Ping SUCCESS \t '
            oeversion = getVNXfirmware(vnx.strip(), "admin", "password")
            logger.info(f"===>Unisphere Version : {oeversion}")
            # res = enm_id + " :\t" + pingresult + "\t" + "VNX OE Version :" + str(oeversion)
            res = f'{enm_id} :\t {pingresult} \t VNX OE Version :{str(oeversion)} \r'
            yield res
        else:
            pingresult = f'{enm_id} :{vnx.strip()} \t Ping FAILED '
            logger.info(pingresult)
            yield pingresult
        try:
            vnxfirmare_log.writelines(res)
        except Exception as e:
            logger.debug(f'caught {type(e)}: e')
    vnxfirmare_log.close()
    return

    # return


def switch(hardwaremodel):
    hardwaremodel = str(hardwaremodel)
    logger.debug(f"switch hardwaremodel: {hardwaremodel}")
    if "VNX" in hardwaremodel:
        for i in getVNXlist(hardwaremodel):
            print(i)
    elif "UNITY" in hardwaremodel:

        # getUnitylist isa generator
        for i in getUnitylist(hardwaremodel):
            print(i)
    return


def main(opts, args):
    if "-s" in opts:
        logger.debug(args)
        logger.info(f"==============={args}===============")
        switch(args)
    elif "-n" in opts:
        logger.info(" ".join(arg.upper() for arg in args))
        # TODO specify individual hosts
    elif "-l" in opts:
        logger.info("# ".join(arg.lower() for arg in args))
        get_ENMids_owning(args[0])

        # TODO
    elif "-t" in opts:
        logger.info(" ".join(arg.lower() for arg in args))
        # TODO logger.info out ENM id : fqdn <SUCCESS|ERROR> : firmware version
    elif "-v" in opts:
        logger.info("================================= Unity 450F ====================")
        hw_model = "EMC UNITY 450F"
        switch(hw_model)

    else:
        raise SystemExit(f"Usage: {sys.argv[0]} (-s | -u | -l) <arguments>...{opts}")


# def test_getUnitylist():
#     assert not getUnitylist("EMC UNITY 450F")


if __name__ == '__main__':
    logger = activate_logging()
    logger.debug("in --if main --")
    #getListofhardware( "EMC UNITY 450F", dns_suffix=".athtem.eei.ericsson.se")
    getListofhardware( "EMC VNX5400 DPE", dns_suffix=".athtem.eei.ericsson.se")
    main("-s", "EMC UNITY 450F")
    main("-s","EMC VNX5400 DPE")
    #logger.info(get_ENMids_owning("ieatvnx-77".upper()))
    #logger.info(get_ENMids_owning("ieatunity-12".upper()))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
