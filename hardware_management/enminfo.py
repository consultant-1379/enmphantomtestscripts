import os
import re
import sys

import definitions
import hpeinfo
import requests
import json
import pandas as pd
import platform  # For getting the operating system name
import subprocess  # For executing a shell command
import inspect
import logging
from definitions import DATA_PATH

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
if not opts:
    opts = "-v"
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]


# eris_file = DATA_PATH + "eris_export_ENM_200123.xlsx"
#eris_file = DATA_PATH + "eris_export_ENM_test.xlsx"
eris_file = DATA_PATH + "ERIS export for ENM 200323.xlsx"

def get_eris_file():
    return eris_file
sheet = "Sheet1"
global logger


def activate_logging(logname="hardware_management.log"):
    logging.basicConfig(filename= definitions.LOG_ROOT + logname,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    # Create a StreamHandler and add it to the root logger
    console_handler = logging.StreamHandler()
    logging.getLogger().addHandler(console_handler)
    global logger
    logger = logging.getLogger(__name__)
    logger.debug(f"activate_logging({logname})")
    return logger

def get_eris_data_as_df():
    # TODO this should take a filter as argument
    df = pd.read_excel(io=get_eris_file(), sheet_name=sheet, dtype="string", engine='openpyxl', )
    df = df.apply(lambda x: x.astype(str).str.upper())
    select_cols = ['Testplan Name', 'CI Name', 'Functional designation']
    df = df[select_cols]
    return df

# define a filter function
def filter_dataframe(df, filter_expr):
    filtered_df = df.loc[filter_expr]
    return filtered_df


def get_enm_hosts(Test_plan_name):
    df = get_eris_data_as_df()


def get_ENMids_owning(this_hostname):
    # this_hostname="IEATUNITY-12"
    # logger = activate_logging()
    df = get_eris_data_as_df()
    # result = df[df.isin([this_hostname]).any(axis=1)]
    result = df[df["CI Name"].isin([this_hostname])]
    logger.info(f"get_ENMids_owning({this_hostname})  : result1 =  {str(result)}")
    if result.empty:
        logger.warning(f'\rdf result is empty for {this_hostname}')
        column_list = []
    else:
        column_list = result['Testplan Name'].tolist()
        numeric_id_required = False
        if numeric_id_required:
            for i in range(len(column_list)):
                column_list[i] = str(column_list[i]).split("_", )[1]  # just return the ENM numeric id
    logger.info(f"get_ENMids_owning({this_hostname}) : column_list =, {column_list}")
    return column_list

def getListofhardware(functional_designation, dns_suffix=".athtem.eei.ericsson.se"):
    # todo Move dns_suffix addition to more suitable function
    logger.info("getListofhardware")
    df = get_eris_data_as_df()
    df["CI Name"] = df["CI Name"] + dns_suffix
    result = df[df["Functional designation"].isin(
        [functional_designation])]  # get rows for functional designation e.g. EMC UNITY 450F
    # remove leading and trailing spaces from all string columns
    # df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # # replace \n  within the string columns with an empty string
    # df = df.apply(lambda x: x.str.replace('\n', '') if x.dtype == "object" else x)
    #logger.info("\ngetListofhardware:", str(result["CI Name"]))
    result = result['CI Name'].to_string(index=False) #.lower()  # extract just the list of CI Names
    result =result.split("\n")
    # remove spaces within each string element
    result = [s.replace(' ', '') for s in result]
    result = [s.lower() for s in result]
    logger.info(f"getListofhardware: {result}")
    return (result)


def get_list_of_hosts(testplan_name):
    logger.info(f"get_list_of_hosts({testplan_name})")
    df = get_eris_data_as_df()
    hosts_filter = (df['Testplan Name'] == testplan_name) & (df['Functional designation'].str.contains('PROLIANT'))
    listofhosts = filter_dataframe(df,hosts_filter)
    listofhosts = listofhosts['CI Name'].tolist()
    return listofhosts



if __name__ == '__main__':
    logger = activate_logging()
    logger.debug("in --if main --")
    #logger.debug(get_list_of_hosts('ENM_51078_EEIDLE_D&S'))
    #logger.debug(listofhosts.tolist())
    # TODO get firmware for each server
    ENM_List = ['ENM_51071_EEIDLE_D&S','ENM_51073_EEIDLE_D&S','ENM_51074_EEIDLE_D&S','ENM_51075_EEIDLE_D&S','ENM_51076_EEIDLE_D&S','ENM_51077_EEIDLE_D&S','ENM_51078_EEIDLE_D&S']
    ENM_List = ['ENM_51076_EEIDLE_D&S','ENM_51077_EEIDLE_D&S']
    ENM_LIST = ['ENM_51081_ZKARPAV_A&O','ENM_51080_ZKARPAV_A&O','ENM_51088_ZVENKAL_TNNI']
    #ENM_List = ['ENM_51078_EEIDLE_D&S']
    ENM_List = ['ENM_51071_EEIDLE_D&S','ENM_51073_EEIDLE_D&S','ENM_51074_EEIDLE_D&S','ENM_51075_EEIDLE_D&S','ENM_51076_EEIDLE_D&S','ENM_51077_EEIDLE_D&S','ENM_51078_EEIDLE_D&S','ENM_51079_EEIDLE_D&S','ENM_51080_ZKARPAV_A&O' ,'ENM_51081_ZKARPAV_A&O','ENM_51088_ZVENKAL_TNNI','ENM_51108_EEIDLE_D&S','ENM_51110_EEIDLE_D&S','ENM_51111_EEIDLE_D&S','ENM_51112_EEIDLE_D&S','ENM_51114_EEIDLE_D&S','ENM_51118_EEIDLE_D&S']
    #ENM_List = ['ENM_51108_EEIDLE_D&S','ENM_51112_EEIDLE_D&S','ENM_51081_ZKARPAV_A&O']
    with open(definitions.HPE_server_firmware_output, 'w') as file:
        # Insert the Header line at the top of the file
        file.write('Testplan Name:Hostname:Serial Number:Model:Component Name:Description:Id:Firmware Version:\n')
    for ENM in ENM_List:
        for host in get_list_of_hosts(ENM):
            print(host)
            enm = hpeinfo.ENM_ilohost(ENM,host,"root","shroot12")
            if enm.REDFISHOBJ is not None:
               enm.close_session()
    df = pd.read_csv(definitions.HPE_server_firmware_output,sep=":")
    xl =definitions.HPE_server_firmware_output.replace(".csv",".xlsx")
    df.to_excel(xl,index=False)
# # Open the file for writing
# with open(filename, "w") as f:
#     f.write("This is a file with the current date in its name.")

