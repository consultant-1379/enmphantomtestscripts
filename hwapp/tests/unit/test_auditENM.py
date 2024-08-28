import nose2, unittest
import auditENM
from errno import ENOENT

import json
import os


# TODO create centos/redhat docker container with python 2.7 and mount the src directory to allow to execute unit tests
class ENMHostsTests(unittest.TestCase):
    ENMDetails = []

    def setUp(self):
        self.ENMDetails = auditENM.get_enm_details(
            "C:\\Users\\eeidle\\OneDrive - Ericsson\\ENM Test\\ENM20_projects\\tests\\integration\\fixtures\\ENMDetails")
        self.ms, self.enm_data = auditENM.get_management_server("570", self.ENMDetails)  # get specific enm
        print("setup : " + str(self.enm_data))
        self.enm = auditENM.ENM("ieatlms4618.athtem.eei.ericsson.se", self.enm_data)
        # os.chdir("C:\Users\eeidle\OneDrive - Ericsson AB\ENM Test\ENM20_projects\\tests\integration\\fixtures")

    def test_get_management_server(self):

        # ms, enm = auditENM.get_management_server("235", self.ENMDetails)
        self.assertEqual(self.ms, "ieatlms4618.athtem.eei.ericsson.se")
        # self.assertEqual(auditENM.get_management_server(self.enm['ID'], "235"))

    def test_enm_instance_variables(self):
        self.assertEqual(self.enm.root_user, "root")
        self.assertEqual(self.enm.root_password, "12shroot")
        self.assertEqual(self.enm.installation_dir, "/root/.neo")

    # def test_ssh_login_to_lms(self):
    #     self.enm
    #
    #     client = get_ssh_client(host, user=None, password=None, pkey=None, key_filename="/root/.ssh/vm_private_key"):

    def test_get_enm_version(self):
        self.assertEqual("ENM 23.06 (ISO Version: 2.22.60) AOM 901 151 R1GA",self.enm.get_enm_version())

    def test_get_redhat_version(self):
        self.assertEqual(self.enm.get_redhat_version(self.enm.ms),
                          "Red Hat Enterprise Linux Server release 6.10 (Santiago)")

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
        sftp, transport = auditENM.get_sftp_session(self.ms, "root", "12shroot")

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
        if self.enm.installation_dir:  # 'installation_dir']
            remote_filepath = str(self.enm.installation_dir)
            remote_file = str(self.enm.installation_dir) + os.altsep + local_filename
        else:
            raise IOError(ENOENT, 'Issue with installation directory', self.enm.installation_dir)
        if sftp_exists(sftp,remote_filepath):
            remoteFiles = sftp.listdir(path=remote_filepath)
            print(remote_filepath + " " + str(remoteFiles))
            for file in remoteFiles:
                sftp.remove(remote_filepath +"/" +file)
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
                os.path.join("C:\\Users\\eeidle\\OneDrive - Ericsson\\ENM Test\\ENM20_projects\\tests\\unit","test_mycode.py")))

    def test_start_centos_docker_image(self): #TODO
        """:returns starts image
        setup file share for src,data and output
        setup networking
        install needed packages
        The docker image should be used for unit
        """
        pass

    def test_no_weak_ciphers(self):  # TODO
        result = self.enm.install_nmap_for_ciphers(self.ms)
        print("result of nmap install = {}".format(result))


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ENMHostsTests)
    unittest.TextTestRunner(verbosity=5).run(suite)
