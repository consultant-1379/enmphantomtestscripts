import sys, os
sys.path.append("/usr/src/app/src")
import nose2, unittest
import auditENM
from errno import ENOENT
import shelve
import os
import ENM

""" Run from docker image as shown below
# /usr/src/app/src # python3 ../tests/unit/test_auditENM2.py
"""
# TODO create centos/redhat docker container with python 2.7 and mount the src directory to allow to execute unit tests
class ENMHostsTests(unittest.TestCase):
    ENMDetails = []

    def setUp(self):
        db = shelve.open('class-shelve')
        for key in db:
            # key is enm id
            self.enm = db[key]
            self.enm.set_admin_user("root")
            self.enm.set_admin_user_password("12shroot")
            print(self.enm.ms)
            db[key] = self.enm
            print(" db2", db[key].get_all_attrs())
        db.close()

    def test_get_management_server(self):

        # ms, enm = auditENM.get_management_server("235", self.ENMDetails)
        self.assertIn(".athtem.eei.ericsson.se", self.enm.ms)
        # self.assertEqual(auditENM.get_management_server(self.enm['ID'], "235"))

    def test_enm_instance_variables(self):
        self.assertEqual(self.enm.admin_user, "root")
        self.assertEqual(self.enm.admin_user_password, "12shroot")
        self.assertEqual(self.enm.installation_dir, "/root/.neo")

    # def test_ssh_login_to_lms(self):
    #     self.enm
    #
    #     client = get_ssh_client(host, user=None, password=None, pkey=None, key_filename="/root/.ssh/vm_private_key"):

    def test_get_enm_version(self):
        print("....", self.enm.ms)
        self.assertIn("ENM 23", self.enm.get_enm_version(self.enm.ms))
        # failing because file doesnt exist
        #self.assertIn("ENM 22", self.enm.get_enm_version("ieatlms4906.athtem.eei.ericsson.se"))
        # self.assertEqual("ENM 20.16 (ISO Version: 1.100.161) AOM 901 151 R1DY/13",self.enm.get_enm_version())

    def test_get_lms_version(self):
        print("....", self.enm.ms)
        hwver=[]
        hwver= ENM.exec_shell_command(self.enm.ms,22,'dmidecode | grep -A3 -i "System Information"| grep "Product Name"',"12shroot")
        print("Hardware :",hwver[0])
        self.assertIn("Gen9",hwver[0])

    def test_get_redhat_version(self):
        self.assertEqual("Red Hat Enterprise Linux Server release 7.9 (Maipo)",
                         self.enm.get_redhat_version(self.enm.ms),
                         )
        # "Red Hat Enterprise Linux Server release 6.10 (Santiago)")

    def test_get_java_version(self):
        self.assertEqual(self.enm.get_java_version(self.enm.ms),
                         "Java(TM) SE Runtime Environment (build 1.8.0_261-b25)")

    # def test_sftp_push_to_server(self,local_filepath,remote_filepath): #TODO convert to data driven
    def sftp_exists(sftp, path):
        try:
            sftp.stat(path)
            return True
        except FileNotFoundError:
            return False

    def test_sftp_push_to_server(self, ):  # TODO convert to data driven
        sftp, transport = auditENM.get_sftp_session(self.enm.ms, "root", "12shroot")

        def sftp_exists(sftp, path):
            try:
                sftp.stat(path)
                return True
            except FileNotFoundError:
                return False

        local_path = 'c:\\users\\eeidle\\onedrive - ericsson\\enm test\\enm20_projects\\src'
        local_filename = "auditENM.py"
        local_filepath = os.path.join(local_path, local_filename)
        local_filepath = 'c:\\users\eeidle\onedrive - ericsson\enm test\enm20_projects\src\\auditENM.py'
        local_filepath = str(os.getcwd())+ "/" + local_filename
        if self.enm.installation_dir:  # 'installation_dir']
            print("self.enm.installation_dir:",self.enm.installation_dir)
            remote_filepath = str(self.enm.installation_dir)
            remote_file = self.enm.installation_dir + str(os.altsep) + local_filename
        else:
            raise IOError(ENOENT, 'Issue with installation directory', self.enm.installation_dir)
        if sftp_exists(sftp, remote_filepath):
            remoteFiles = sftp.listdir(path=remote_filepath)
            print(remote_filepath + " " + str(remoteFiles))
            for file in remoteFiles:
                sftp.remove(remote_filepath + "/" + file)
            sftp.rmdir(path=remote_filepath)
        print(remote_filepath)
        print(local_filepath)
        print(sftp.listdir("/root"))
        sftp.mkdir(remote_filepath)
        print(sftp.listdir("."))
        sftp.put(local_filepath, remote_file)
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        self.assertTrue(
            os.path.isfile(
                "ENM.py"))
                #os.path.join("C:\\Users\\eeidle\\OneDrive - Ericsson\\ENM Test\\ENM20_projects\\tests\\unit",
                #os.path.join(os.getcwd() + "../tests/unit",                              "test_mycode.py")))

    def test_start_centos_docker_image(self):  # TODO
        """:returns starts image
        setup file share for src,data and output
        setup networking
        install needed packages
        The docker image should be used for unit
        """
        pass

    def test_no_weak_ciphers(self):  # TODO
        result = self.enm.install_nmap_for_ciphers(self.enm.ms)
        print("result of nmap install = {}".format(result))


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ENMHostsTests)
    unittest.TextTestRunner(verbosity=5).run(suite)
