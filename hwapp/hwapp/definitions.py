import os
import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep #+ os.pardir
#ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)) # This is your Project Root
#print("root dir ",ROOT_DIR)
#DATA_PATH = 'C:\\Users\\<user>\\Downloads\\' if platform.system().lower() == 'windows' else './'
#DATA_PATH = 'data\\' if platform.system().lower() == 'windows' else 'data\/'
DATA_PATH = os.path.join(ROOT_DIR, 'data' + os.sep)
#eris_file = DATA_PATH + "ERIS export for ENM 200323.xlsx"
eris_file = DATA_PATH + 'ERIS export for ENM 150523.xlsx'
LOG_ROOT = ROOT_DIR + os.sep + "logs" + os.sep
HTTPD_CONF_DIR="/etc/httpd/conf/"
CGI_DIR="/var/www/cgi-bin/"
HTTPD_DocumentRoot="/var/www/html"
# log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir), 'logs')
# log_fname = os.path.join(log_dir, 'log_file_name.log')

now = datetime.datetime.now()
# Format the date as a string in the format of your choice
date_str = now.strftime("%d-%m-%y_%H-%M")
# Create the filename with the date in it
HPE_server_firmware_output = LOG_ROOT + f"HPE_server_firmware_{date_str}.csv"


# ilo_host = "ieatlms3841ilo.athtem.eei.ericsson.se"
# ilo_host = "ieatvio025ilo.athtem.eei.ericsson.se"
# ilo_host = "ieatrcx8141lo.athtem.eei.ericsson.se"
#ilo_host = "ieatrcx8045ilo.athtem.eei.ericsson.se"
# ilo_host = "ieatlms8146ilo.athtem.eei.ericsson.se"
ilo_host = "ieatlms8290ilo.athtem.eei.ericsson.se"
ilo_host = "ieatrcx8045ilo.athtem.eei.ericsson.se"
ilo_host = "ieatlms8149ilo.athtem.eei.ericsson.se" #smart array
ilo_host = "ieatrcx8125ilo.athtem.eei.ericsson.se" #HBA

ilo_username = 'root'
ilo_password = 'shroot12'
base_url = 'https://' + ilo_host
server_url = base_url + '/redfish/v1/systems/1'
SYSTEM_URL = base_url
LOGIN_ACCOUNT = ilo_username
LOGIN_PASSWORD = ilo_password