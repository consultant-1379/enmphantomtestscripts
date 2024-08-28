import nose2, unittest
import auditENM
import getLMShostname
from errno import ENOENT

import json
import os


# TODO create centos/redhat docker container with python 2.7 and mount the src directory to allow to execute unit tests
class ENMHostsTests(unittest.TestCase):
    ENMDetails = []
    os.chdir("C:\\Users\\eeidle\\OneDrive - Ericsson\\ENM Test\\ENM20_projects\\tests\integration\\fixtures")
    path=os.getcwd()
    ENMs=path +os.altsep +"ENMs.json"
    ENMdeployments=path +"\\" + "ENMdeployments.json"
    def setUp(self):

        # self.ENMDetails = auditENM.update_enm_details(
        #     "C:\\Users\\eeidle\\OneDrive - Ericsson\\ENM Test\\ENM20_projects\\tests\\integration\\fixtures\\ENMs.json")
        #self.ms, self.enm_data = auditENM.get_management_server("596", self.ENMDetails)  # get specific enm
        #print(self.enm_data)
        #self.enm = auditENM.ENM("ieatlms4616.athtem.eei.ericsson.se", self.enm_data)
        result=[]
        result=self.populate_ENMList()
        print(result)
        for enm in result:
            enmid =enm[0]
            print(enmid)
            ms=enm[1]
            auditENM.update_enm_details(self.ENMdeployments,ENMid=enmid,ms=ms)

    def get_ENMids(self, json_file):

        import json
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data

    def populate_ENMList(self):
        from multiprocessing import Pool
        with Pool() as pool:
            result = pool.map(getLMShostname.getMyLMS, self.get_ENMids(self.ENMs))
            return(result)


    def initial_setup_of_ENMList(self):
        # Serializing json
        import json
        dictionary = (
            '1071', '1072', '1073', '1074', '1075', '1076', '1077', '1078', '1079', '1080', '1081', '1088', '1088',
            '596', '404', '431', '441', '223', '320', '321', '335'
        )
        json_object = json.dumps(dictionary, indent=4)
        os.chdir("C:\\Users\EEIDLE\\OneDrive - Ericsson\\ENM Test\\ENM20_projects\\tests\integration\\fixtures")
        # Writing to sample.json
        with open("ENMs.json", "w") as outfile:
            outfile.write(json_object)


    def test_start_centos_docker_image(self): #TODO
        """:returns starts image
        setup file share for src,data and output
        setup networking
        install needed packages
        The docker image should be used for unit
        """
        pass

    def test_no_weak_ciphers(self):  # TODO
        #result = self.enm.install_nmap_for_ciphers(self.ms)
        #print("result of nmap install = {}".format(result))
        pass


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ENMHostsTests)
    unittest.TextTestRunner(verbosity=5).run(suite)
