import nose2, unittest
import auditENM
import json, objectpath

import os


# TODO create centos/redhat docker container with python 2.7 and mount the src directory to allow to execute unit tests
def get_by_attr(mylist, key, value):
    for item in mylist:
        if item[key] == value:
            return item
    raise KeyError('no match found')  # raise an exception instead of silently returning None


class ENMHostsTests(unittest.TestCase):
    class ENM:
        def __init__(self, ms, enm):
            self.enm = enm
            self.ms = ms
            self.root_user = "user"
            self.root_password = "password"
            self.installation_dir = ""
            self.enm_version = ""
            self.java_version = commands.getoutput('java -version')
            self.os_version = commands.getoutput('cat /etc/redhat-release')
            self.__init_me__()

        def get_user_password(self):
            return self.root_password

        def set_root_user(self):
            self.root_user = self.enm['root']

        def set_installation_dir(self):
            self.installation_dir = self.enm['installation_dir']

        def get_root_user(self):
            return self.root

        def set_user_password(self):
            self.root_password = self.enm['root_password']

        def __init_me__(self):
            self.set_root_user()
            self.set_user_password()
            self.set_installation_dir()

        def get_enm_version(self):
            print(exec_shell_command(self.ms, 22, "cat /etc/enm-version", self.root_password))
            self.enm_version = exec_shell_command(self.ms, 22, "cat /etc/enm-version", self.root_password)
            # {"litp_version": ""},
            # {"deployment_description": ""},
            # {"ip_versions": ""},
            # {"DDC_configured": ""}


if __name__ == '__main__':
    unittest.main()
