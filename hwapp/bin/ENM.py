import requests
from bs4 import BeautifulSoup
import paramiko


# database
# db = {}
# db[ENMid] = {
#     "ms": ms + ".athtem.eei.ericsson.se",
#     "root": "root",
#     "root_password": "12shroot",
#     "litp-admin_password": "12shroot",
#     "installation_dir": "/root/.neo",
#     "ENM_type": "LITP",
#     "java_version": "",
#     "os_version": "",
#     "enm_version": "",
#     "litp_version": "",
#     "deployment_description": "",
#     "ip_versions": "",
#     "DDC_configured": ""
# }
class ENM:
    def __init__(self, enm, ms=None, admin_user=None, admin_user_password=None):
        self.enm = enm
        self.ms = ms
        self.admin_user = admin_user
        self.admin_user_password = admin_user_password
        self.installation_dir = "/root/.neo"
        # self.java_version = commands.getoutput('java -version')
        # self.os_version = commands.getoutput('cat /etc/redhat-release')
        # self.__init_me__()

    def set_installation_dir(self,installation_dir):
        self.installation_dir = installation_dir

    def set_admin_user(self, admin_user):
        self.admin_user = admin_user

    def get_admin_user(self):
        return self.admin_user

    def set_admin_user_password(self, admin_user_password):
        self.admin_user_password = admin_user_password

    def get_admin_user_password(self):
        return self.admin_user_password

    def __str__(self):
        return ('<%s => %s: MS => %s>' %
                (self.__class__.__name__, self.enm, self.ms))

    def get_all_attrs(self):
        return ('<%s => %s: MS => %s> :adminuser => %s: adminpassword => %s' %
                (self.__class__.__name__, self.enm, self.ms, self.get_admin_user(), self.get_admin_user_password()))
    # def __init_me__(self):
    #     self.set_root_user()
    #     self.set_user_password()
    #     self.set_installation_dir()

    def get_enm_version(self, host):
        # print(exec_shell_command(self.ms, 22, "cat /etc/enm-version", self.admin_user_password))
        enm_version = exec_shell_command(host, 22, "cat /etc/enm-version", self.admin_user_password)
        filenotfound= []
        if enm_version == filenotfound:
            return "WARN:enm-version file does not exist"
        enm_version = str(enm_version[0]).rstrip()
        return str(enm_version)

    def get_redhat_version(self, host):
        redhat_version = exec_shell_command(host, 22, "cat /etc/redhat-release", self.admin_user_password)
        redhat_version = str(redhat_version[0]).rstrip()
        return redhat_version

    def get_java_version(self, host):
        java_version = exec_shell_command(host, 22,
                                          "java -version > /tmp/java_version.tmp  2>&1 && grep -e \"Java(TM) SE "
                                          "Runtime Environment\" /tmp/java_version.tmp && rm -f "
                                          "/tmp/java_version.tmp",
                                          self.admin_user_password)
        java_version = str(java_version[0]).rstrip()
        return java_version

    def install_nmap_for_ciphers(self, host):
        result = exec_shell_command(host, 22,
                                    "rpm -vhU https://nmap.org/dist/nmap-7.80-1.x86_64.rpm && curl "
                                    "https://svn.nmap.org/nmap/scripts/ssl-enum-ciphers.nse -o ssl-enum-ciphers.nse &&"
                                    " curl  https://svn.nmap.org/nmap/scripts/ssh2-enum-algos.nse -o ssh2-enum-algos.nse &&"
                                    " curl https://svn.nmap.org/nmap/scripts/ajp-request.nse",
                                    self.admin_user_password)
        return result

def exec_shell_command(host, port, cmd, password, user="root", sshKey=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if sshKey:
        ssh.connect(host, username=user, key_filename=sshKey, port=port)
    else:
        ssh.connect(host, username=user, password=password, port=port)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    response = stdout.readlines()
    return response

def getLMS(url):
    # Gets LMS from scraping the DMT page specified in url
    # Create object page
    page = requests.get(url)
    # parser-lxml = Change html to Python friendly format
    # Obtain page's information
    soup = BeautifulSoup(page.content, 'lxml')
    # Obtain information from tag <table>
    # <table class="deployment-table"><tbody><tr><th>ID</th><td>1081</td></tr><tr><th>Description</th><td>Icelake #10
    # CIS-149689</td></tr><tr><th>MAC Range</th><td>None - None</td></tr><tr><th>Group</th><td>Not Set <a class="img" href="/dmt/changeClusterGroupOnCluster/1081/"><img src="/static/images/edit.png" alt="Edit the Cluster Group this node is defined against" height="18" width="18"></a></td></tr><tr><th>RA</th><td>ENM --&gt; Deployment</td></tr><tr><th>Layout</th><td>KVM</td></tr><tr><th>ENM Deployment Type</th><td>Extra_Large_ENM_On_Rack_Servers</td></tr><tr><th>IP Version</th><td>Dual</td></tr><tr><th>Management Server</th><td><a href="/dmt/mgtsvrs/90805/">ieatlms8147 (id: 524)</a></td></tr><tr><th>Deployment Description</th><td><a class="img" href="/dmt/deploymentUpdatedReport/1081/">Reports</a><div class="table-actions"><form id="ddUpdateForm" method="post" action="/api/deployment/updateClustersServicesWithDD/1081/"><a class="img" href="/dmt/1081/deploymentDescription/edit/"><img src="/static/images/edit.png"></a><a class="img" href="javascript:void(0)" onclick="checkFormAction('Do you really want to Refresh the DMT for this Cluster using the Deployment Description? This will overwrite the current settings on this Cluster\n\nNOTE: This may take a few minutes for a complete update of the cluster', 'ddUpdateForm');"><img src="/static/images/refresh.svg" title="Refresh Cluster Settings using configured Deployment Description"></a><a class="img" href="javascript:void(0)" onclick="checkAction('Do you really want to Delete this Deployment Description Mapping?','/dmt/1081/deploymentDescription/delete/');"><img src="/static/images/delete.png"></a></form></div><table class="deployment-description-table"><tbody><tr><th>Version</th><td>2.16.4</td></tr><tr><th>Type</th><td>rpm</td></tr><tr><th>Capacity Type</th><td>production</td></tr><tr><th>Name</th><td>ENMOnRack__production_dualStack__5evt</td></tr><tr><th>Auto Update</th><td> Yes </td></tr><tr><th>Update Type</th><td>partial</td></tr><tr><th>Ip Range Source</th><td>manual</td></tr></tbody></table></td></tr></tbody></table>
    for row in soup.table.find_all('tr'):
        if (row.text.find("Management Server") > -1):
            # row_name = row.th.get_text()
            row_value = row.td.get_text()
            # >ieatlms8147 (id: 524)<
            seperator = " "
            ms = row_value.split(seperator, 1)[0]
            return (ms)


def getLMSfromDMT(enm):
    # Create an URL object
    url = 'https://ci-portal.seli.wh.rnd.internal.ericsson.com/dmt/clusters/' + enm
    # return enm and lms
    return (enm, getLMS(url))

def getOmbsDetails(enm):
    pass
def getENIQDetails(enm):
    pass


if __name__ == '__main__':
    # with httpd apache2 running mount {definitions.HTTPD_DocumentRoot}/htdocs/ on docker image
    # enm596 = ENM("596","ieatlms7480")
    enm596 = ENM("596", "ieatlms4906.athtem.eei.ericsson.se", "root", "12shroot")
    # enm431 = ENM("431", "ieatlms5741", 'root', '12shroot')
    # enm404 = ENM("404")
    print(enm596)
    print(enm596.admin_user_password)
    print(enm596.ms)
    print(enm596.get_enm_version(enm596.ms))
    print(enm596.get_redhat_version(enm596.ms))
