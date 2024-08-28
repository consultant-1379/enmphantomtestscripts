# import jinja2
# requires pandas, openpyxl
import os
import re
import sys
import requests
import json
import platform  # For getting the operating system name
import subprocess  # For executing a shell command
import inspect
import logging

import definitions
from definitions import DATA_PATH
from logger.logger import activate_logging as activate_logging
import enminfo
#from enminfo.enminfo import get_ENMids_owning,getListofhardware

# logname="log21.log"
#
#
# logging.basicConfig(filename=logname,
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
if not opts:
    opts = "-v"
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

global logger
logger = activate_logging()
eris_file = DATA_PATH + "ERIS export for ENM 200323.xlsx"
eris_file = DATA_PATH + "eris_export_ENM_test.xlsx"
#
#
# def activate_logging(logname="logging_saninfo.log"):
#     logging.basicConfig(filename=logname,
#                         filemode='a',
#                         format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                         datefmt='%H:%M:%S',
#                         level=logging.DEBUG)
#     # Create a StreamHandler and add it to the root logger
#     console_handler = logging.StreamHandler()
#     logging.getLogger().addHandler(console_handler)
#     global logger
#     logger = logging.getLogger(__name__)
#     logger.debug("activate_logging")
#     return logger
#
# def get_eris_file():
#     return eris_file
sheet = "Sheet1"
# unity_creds = (
#     327, 12, "admin/Password123#", "5.1.2.0.5.007",
#     12, 18, "root/shRoot12!",
#     12,15, "admin/Password123!", "5.1.2.0.5.007",
#     19, "root/Password123_",
#     1, 7, 3, 18, 19, 24, 29, 25, 26, 31, 34, 36, 37, 41, 42, 43, 44, 47, 49, "admin/Password1234#",
#     27, 50, 375, "admin/Password1234_",
#     7, "localadmin/Password123_",
#     35, "admin/Password1234",
#     12, 38, "localadmin/Password1234#",
# )
#
#
# def getHostnames(df):
#     print("unused function")  # TODO
#     df = df.set_index(['Functional designation'])  # set index on Product Model
#     result = df.loc['EMC UNITY 450F']  # on F only return on this filter
#     # result= result.iloc[:,[0,2]]      # return all rows and only columns 0 and  2 in result
#     result = result.loc[:, ['Testplan Name', 'CI Name']]  # return all rows and only columns A and C in result
#     return result
#
# def get_ENMids_owning_(this_hostname):
#     #this_hostname="IEATUNITY-12"
#     df = pd.read_excel(io=eris_file, sheet_name=sheet, dtype="string", engine='openpyxl', )
#     select_cols = ['Testplan Name', 'CI Name', 'Functional designation']
#     df = df[select_cols]
#     result = df[df.isin([this_hostname]).any(axis=1)]
#     result = df[df["CI Name"].isin([this_hostname])]
#     print("get_ENMids_owning:",result)
#     if result.empty:
#         print('df result is empty')
#         result = ""
#     else:
#         result = result["Testplan Name"].to_string(index=False) #test plan name ENM_5596_EEIDLE_D&S
#         result= result.split("_",)[1]
#     print(result)
#     return (result)
#
#
# def get_ENMids_owning(this_hostname):
#     # this_hostname="IEATUNITY-12"
#     # logger = activate_logging()
#     #this_hostname="IEATVNX-77"
#     if "VNX" in this_hostname:
#         this_hostname = this_hostname[:-3]
#     logger.info(f"this_hostname :=  {str(this_hostname)}")
#
#     df = pd.read_excel(io=get_eris_file(), sheet_name=sheet, dtype="string", engine='openpyxl', )
#     select_cols = ['Testplan Name', 'CI Name', 'Functional designation']
#     df = df[select_cols]
#     # result = df[df.isin([this_hostname]).any(axis=1)]
#     result = df[df["CI Name"].isin([this_hostname])]
#     logger.info(f"get_ENMids_owning : result1 =  {str(result)}")
#     if result.empty:
#         logger.warning(f'\rdf result is empty for {this_hostname}')
#         column_list = []
#     else:
#         column_list = result['Testplan Name'].tolist()
#         numeric_id_required = False
#         if numeric_id_required:
#             for i in range(len(column_list)):
#                 column_list[i] = str(column_list[i]).split("_", )[1]  # just return the ENM numeric id
#     logger.info(f"get_ENMids_owning : column_list =, {column_list}")
#     return column_list

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    logging.debug(f"subrocess.run command is :{str(command)}")
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
                return (oeversion, oe_fullversion)

def getUnityVersion(unityurl):
    # with open("C:\\Users\\EEIDLE\\Downloads\\327_basicSystemInfo.json",'r') as string:
    #     my_dict=json.load(string)
    # string.close()
    # iterate_multidimensional(my_dict)
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

# def getListofhardware(functional_designation, dns_suffix=".athtem.eei.ericsson.se"):
#     # todo Move dns_suffix addition to more suitable function
#     df = pd.read_excel(io=get_eris_file(), sheet_name=sheet, dtype="string", engine='openpyxl', )
#     select_cols = ['Testplan Name', 'CI Name', 'Functional designation']
#     df = df[select_cols]
#     df["CI Name"] = df["CI Name"] + dns_suffix
#     result = df[df["Functional designation"].isin([functional_designation])]  # get rows for functional designation e.g. EMC UNITY 450F
#     print("getListofhardware:",result["CI Name"])
#     result = result['CI Name'].to_string(index=False) # extract just the list of CI Names
#     result = str.lower(result)
#     return (result)


class SAN:
    def __init__(self, fqdn, admin_user=None, admin_user_password=None):
        self.fqdn = fqdn
        self.user = admin_user
        self.password = admin_user_password

    def getUnisphereVersion(self):
        print("define me in SAN Subclasses")


class VNX(SAN):
    def __init__(self, fqdn, model, admin_user=None, admin_user_password=None):
        super().__init__(fqdn, admin_user=None, admin_user_password=None)
        self.model = model

    def getUnisphereVersion(self):
        print("DEBUG: cwd for function: " + inspect.currentframe().f_code.co_name, os.getcwd())
        cmd = 'c:\\Program Files (x86)\\EMC\\Navisphere CLI\\NaviSECCli.exe' if platform.system().lower() == 'windows' \
            else '/opt/Navisphere/bin/naviseccli'
        #, "-User","admin", "-Password", "password", "-Scope global", "-Address", "ieatvnx-77spa.athtem.eei.ericsson.se" getagent -rev
        command = [cmd, "-User", self.user, "-Password", self.password, "-Scope global",
                   "-Address",
                   self.fqdn, "getagent -rev"]
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        # output = subprocess.Popen(command).communicate()[0]
        return output.strip().decode('utf-8')


class Unity(SAN):
    def __init__(self, fqdn, model, admin_user=None, admin_user_password=None):
        super().__init__(fqdn, admin_user=None, admin_user_password=None)
        self.model = model

    def getUnisphereVersion(self):
        pass


def getUnitylist(hardwaremodel):
    logger.info("getUnitylist")
    logger.debug(f"getUnitylist: {hardwaremodel}")
    #hw_list = getListofhardware(eris_file, hardwaremodel)
    hw_list = enminfo.getListofhardware(hardwaremodel, dns_suffix=".athtem.eei.ericsson.se")

    #print(unity_creds)
    print(hw_list)
    print("DEBUG: cwd for function: " + inspect.currentframe().f_code.co_name, os.getcwd())
    unityfirmare_log = open(definitions.LOG_ROOT + "unityfirmware.log", "w")
    for line in hw_list:
        enm_id = enminfo.get_ENMids_owning(line.strip().split(".")[0].upper())
        logger.info(f"{enm_id}")
        if ping(line.strip()):
            pingresult = f'{line.strip()} \t Ping SUCCESS \t '
            # logger.info(pingresult, end="\t")
            oeversion, oefullversion = getUnityVersion(line.strip())
            logger.info(f"{enm_id}, {pingresult}    Unity OE Version :   {oeversion} Full Version : {oefullversion}")
            res = f'{enm_id}\t{pingresult}\t{str(oeversion)}\t{str(oefullversion)}\r'
            yield res
        else:
            pingresult = f'{enm_id} :{line.strip()} \t Ping FAILED '
            logger.error(pingresult)
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

def getVNXfirmware_(fqdn, user, password):
    # /opt/Navisphere/bin/naviseccli -User admin -Password password -Scope global -Address ieatvnx-151spa.athtem.eei.ericsson.se getagent | grep "Revision:"
    # Revision:            05.33.021.5.256
    cmd = 'c:\\Program Files (x86)\\EMC\\Navisphere CLI\\NaviSECCli.exe' if platform.system().lower() == 'windows' \
        else '/opt/Navisphere/bin/naviseccli'
    command = [cmd, "-User", user, "-Password",
               password, "-Scope", "global", "-Address",
               fqdn, "getagent", "-rev"]
    try:
        p = subprocess.Popen(command,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #p.stdin.write(b"1")
        output ,err =p.communicate(input=b'1')
        print(output)
        # output = subprocess.Popen(command).communicate()[0]
        return output.strip().decode('utf-8')
    except(FileNotFoundError):
        print(f"ERROR FileNotFoundError : {command} " + inspect.currentframe().f_code.co_name, os.getcwd())
        raise


# def getVNXlist(hardwaremodel):
#     hw_list = getListofhardware(eris_file, hardwaremodel, dns_suffix="spa.athtem.eei.ericsson.se")
#     vnxfirmare_log = open("vnxfirmware.log", "w")
#     #logging.DEBUG(f"hw_list is :{hw_list}")
#
#     for line in hw_list.splitlines():
#         print("line=",line)
#         enm_id = get_ENMids_owning(line.strip().split(".")[0].upper())
#         print("enm_id=",enm_id)
#         if ping(line.strip()):
#             print(line.strip(), "===>Ping Success", end="\t")
#             pingresult = f'{line.strip()} \t Ping SUCCESS \t '
#
#             oeversion = getVNXfirmware(line.strip(), "admin", "password")
#             print("===>Unisphere Version :", oeversion)
#             res= enm_id + " :\t" + pingresult + "\t" + "VNX OE Version :" + str(oeversion)
#             yield res
#         else:
#             pingresult = f'{enm_id} :{line.strip()} \t Ping FAILED '
#             print(pingresult)
#             yield pingresult
#
#         try:
#             vnxfirmare_log.writelines(pingresult)
#         except Exception as e:
#             logging.DEBUG(f'caught {type(e)}: e')
#     vnxfirmare_log.close()
#     return

def getVNXlist(hardwaremodel):
    hw_list = enminfo.getListofhardware(hardwaremodel, dns_suffix="spa.athtem.eei.ericsson.se")
    vnxfirmare_log = open(definitions.LOG_ROOT + "vnxfirmware.log", "w")
    logger.debug(f"hw_list is :{hw_list}")

    for vnx in hw_list:
        logger.info(f"vnx= {vnx}")
        enm_id = enminfo.get_ENMids_owning(vnx.strip().split("spa.")[0].upper())

        logger.info(f"enm_id= {enm_id} {vnx.strip()}"  )
        if ping(vnx.strip() ):
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



def switch(hardwaremodel):
    hardwaremodel = str(hardwaremodel)
    if "VNX" in hardwaremodel:
        getVNXlist(hardwaremodel)
    elif "UNITY" in hardwaremodel:
        getUnitylist(hardwaremodel)
    return


def main(opts, args):
    if "-s" in opts:
        logger.debug(args)
        logger.info(f"==============={args}===============")
        for arg in args:
            print("=================================== ", arg, " ====================")
            switch(arg)
    elif "-n" in opts:
        logger.info(" ".join(arg.upper() for arg in args))
        # TODO specify individual hosts
    elif "-l" in opts:
        logger.info("# ".join(arg.lower() for arg in args))
        enminfo.get_ENMids_owning(args[0])

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


if __name__ == '__main__':
    logger = activate_logging()
    logger.debug(f"in --if main -- {inspect.currentframe().f_code.co_name}() line: {inspect.getframeinfo(inspect.currentframe()).lineno}")
    #getListofhardware( "EMC UNITY 450F", dns_suffix=".athtem.eei.ericsson.se")
    enminfo.getListofhardware("EMC VNX5400 DPE", dns_suffix="spa.athtem.eei.ericsson.se")

    main(opts, args)
    hw_model = "EMC UNITY 450F"
    switch(hw_model)
    # hw_model = "EMC VNX5500 DPE"  # "EMC UNITY 450F"
    # switch(hw_model)
    # print("===================================  VNX 5400 ====================")
    # hw_model = "EMC VNX5400 DPE"  # "EMC UNITY 450F"
    # switch(hw_model)
    # print("===================================  VNX 5200 ====================")
    # hw_model = "EMC VNX5200 DPE"  # "EMC UNITY 450F"
