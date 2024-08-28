import unittest, socket, os
from myCode import *

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
my_data_path = os.path.join(THIS_DIR, os.pardir, 'data_folder/data.csv')


class MyFirstTests(unittest.TestCase):

    def setUp(self):
        self.target_deployment_lms_fqdn = "ieatlms7347.athtem.eei.ericsson.se"
        self.username = "root"
        self.data = [
            {
                "target_deployment_lms_fqdn": "ieatlms7347.athtem.eei.ericsson.se",
                "username": "root",
                "password": "12shroot"
            }
        ]
        try:
            os.remove(os.path.join("\\Users\eeidle\Downloads", "remotepasswd"))
        except:
            print("setup: remotepasswd not found.")

    def test_get_os_environ(self):
        self.assertIn("\\Users\\eeidle", get_os_environ())


    @unittest.skip("not implemented")
    def test_ssh_login(self, target_deployment_lms_ipv6Address):
        self.fail("NOT IMPLEMENTED")


    def test_sftp_login(self):
        self.assertFalse(os.path.isfile(os.path.join("\\Users\eeidle\Downloads", "remotepasswd")))
        sftp, transport = sftp_session(self.target_deployment_lms_fqdn, "root", "12shroot")
        remote_filepath = "/etc/passwd"
        localpath = "\\Users\\eeidle\\Downloads\\remotepasswd"
        sftp.get(remote_filepath, localpath)

        # Upload
        userhome = os.environ['HOMEPATH']
        filepath = "/tmp/foo.log"
        localpath = userhome + "/" + "ganttproject.log"
        sftp.put(localpath, filepath)
        self.assertTrue(os.path.isfile(os.path.join("\\Users\eeidle\Downloads", "remotepasswd")))
        if sftp:
            sftp.close()
        if transport:
            transport.close()

    def test_sftp_push_to_server(self):
        sftp, transport = sftp_session(self.target_deployment_lms_fqdn, "root", "12shroot")
        remote_filepath = "/tmp/mycode.py"
        local_filepath = "\\Users\eeidle\OneDrive - Ericsson AB\ENM Test\ENM20_projects\src\myCode.py"
        sftp.put(local_filepath, remote_filepath)
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        self.assertTrue(
            os.path.isfile(
                os.path.join("\\Users\eeidle\OneDrive - Ericsson AB\ENM Test\ENM20_projects\\tests\unit", "test_mycode.py")))

    def test_lms_redhat_version(self):
        cmd = "cat '/etc/release'"
        output = ssh_command(self.target_deployment_lms_fqdn, 22, cmd, "12shroot")
        print(output)

    def tearDown(self):
        pass


class TestTransferTests(unittest.TestCase):
    def test_TransferTests(self):
        #self.skipTest
        pass

        # self.assertEqual(TransferTests(ieatloaner332.athtem.eei.ericsson.se,22,hostname,"12shroot"),"ieatloaner332")


if __name__ == '__main__':
    unittest.main()
