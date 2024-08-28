##############################################################################################
#!bin/bash                                                                                   #
# Dec    : Script to check all the servers Red-hat release,version,history                   #
##############################################################################################
echo "These are the list of the servers we have it";echo ""
cat server.txt | awk '{ print $1 }';echo "Please enter the vaue that you want...EX..340"; echo " ";read x ; echo $x;cat server.txt | grep -i $x | awk '{print $3}'> result.txt
echo "These are the server details.....";echo " "; cat server.txt | grep -i $x | awk '{print $1,$2,$3}' ;echo " "
for i in `cat result.txt| awk '{ print $1 }'`; do ssh $i -T "cat /etc/redhat-release; echo "Successfully listed Red-Hat Release ......"; echo " "; cat /etc/enm-version; echo "Successfully Listed Current ENM Software Version ......"; echo " "; cat /etc/enm-history";echo "Successfully Listed ENM Software History Details ......"; echo " ";echo " "; done
########################END####################################################################
 
########################## need to give input in below format##################################
#[root@ieatlms4917 test]# cat server.txt
#ENM340 ieatlms4917 141.137.250.11
#ENM596 ieatlms7480 10.210.224.62
#ENM404 ieatlms5218 131.160.148.29
#ENM583 ieatlms5736 10.210.219.122
#ENM431 ieatlms5741 131.160.168.22
#ENM321 ieatlms4895 141.137.244.160
#ENM335 ieatlms4906 141.137.250.251
#[root@ieatlms4917 test]#
###################END##########################################################################