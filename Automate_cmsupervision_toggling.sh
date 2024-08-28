############################################################################################
#!/bin/bash                                                                               #
# Preconditions : Nodes Must Be Added To Both ENM and Workload                             #
# Functionality    : To Toggle CM Supervision for Unsyn nodes                              #                                                                                                                                                                                                    #
# Author : Dhanush, Yaqoob                                                                 #                                                                                                                                                                                                     #
############################################################################################
#Script to sync the unsync nodes with out DB restore(post network rollout)
echo "script modified on 10-oct-2022 "
echo " "
echo "Script Execution Started ..."
echo " "
UNSYNCHRONIZED=`cli_app "cmedit get * CmFunction.syncStatus==UNSYNCHRONIZED -t" | grep -v ESC | grep -v SBG | grep -i unsync >> unsync.txt`
cat unsync.txt | awk '{print $1}' | sort >> unsync1.txt
FILE=unsync1.txt
FILE_WC=`wc -l < $FILE`
FILE_READ=`cat ${FILE}`
echo "$FILE_WC Nodes are in Unsync State"
if [ $FILE_WC -ne 0 ]
        then
                echo "The below nodes are in unsynchronized state ${FILE_READ}"
                echo ""
                while read line
                        do
                                echo "$line"
                cli_app "cmedit set $line CMNodeHeartBeatSupervision active=false"
                sleep 4
                cli_app "cmedit set $line CMNodeHeartBeatSupervision active=true"
                sleep 4
                cli_app "cmedit action $line Cmfunction.syncstatus sync"
                sleep 4
                echo""
                done <unsync1.txt
        else
                echo "Nodes are not in unsynchronized state"
fi
###############################################################################################