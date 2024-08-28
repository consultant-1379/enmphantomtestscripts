##############################################################################################
#!bin/bash                                                                                   #
# Author : Murthy                                                                            #
##############################################################################################
cat /etc/hosts > /home/test/originalhostsfile.txt 
cat /home/test/originalhostsfile.txt |grep -i svc | awk '{ print $1,$2 }' | sort | uniq > /home/test/svc.txt ; cat /home/test/svc.txt | awk '{ print $1 }' > /home/test/svcip.txt 
cat /home/test/originalhostsfile.txt |grep -i db | awk '{ print $1,$2 }' | sort | uniq > /home/test/db.txt ; cat /home/test/db.txt | awk '{ print $1 }' > /home/test/dbip.txt 
cat /home/test/originalhostsfile.txt |grep -i scp | awk '{ print $1,$2 }' | sort | uniq > /home/test/scp.txt ; cat /home/test/scp.txt | awk '{ print $1 }' > /home/test/scpip.txt
for i in `cat /home/test/svcip.txt`; do ssh -i /root/.ssh/vm_private_key cloud-user@$i -T "cat /etc/redhat-release">/home/test/re1.txt ;echo " ";echo " ";echo "SVC IP is..$i ";cat /home/test/re1.txt |awk '{ print $0 }';echo " "; done
for i in `cat /home/test/dbip.txt`; do ssh litp-admin@$i -T "cat /etc/redhat-release" >/home/test/re2.txt ;echo " ";echo " ";echo "DB IP is..$i ";cat /home/test/re2.txt |awk '{ print $0 }';echo " "; done
for i in `cat /home/test/scpip.txt`; do ssh -i /root/.ssh/vm_private_key cloud-user@$i -T "cat /etc/redhat-release">/home/test/re3.txt ;echo " ";echo " ";echo "SCP IP is..$i ";cat /home/test/re3.txt |awk '{ print $0 }';echo " "; done
