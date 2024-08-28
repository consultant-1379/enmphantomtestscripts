##############################################################################################
#!bin/bash                                                                                   #
# Author : Murthy                                                                            #
# Dec    : Script will do all fetch parse create for the netsims in Parallel                 #
##############################################################################################
echo "script got started..."
echo -e '\v**The ,\vscript ,\vgoing to ,\vlist ,\vieatnetsimv' ieatnetsimv$1'**'
/opt/ericsson/nssutils/bin/netsim list ieatnetsimv$1 /var/tmp/arne/ieatnetsimv$1 >>result_ieatnetsimv$1.txt
echo -e '\v**The ,\vscript ,\vgoing to ,\vfetch ,\vieatnetsimv' ieatnetsim$1'**'
/opt/ericsson/nssutils/bin/netsim fetch ieatnetsimv$1 /var/tmp/arne/ieatnetsimv$1 >>result_ieatnetsimv$1.txt
echo -e '\v**The ,\vscript ,\vgoing to ,\vparse ,\vieatnetsimv'$1'**'
/opt/ericsson/nssutils/bin/node_populator parse ieatnetsimv$1 /var/tmp/arne/ieatnetsimv$1 >>result_ieatnetsimv$1.txt
echo -e '\v**The ,\vscript ,\vgoing to ,\vcreate ,\vieatnetsimv'$1'**'
/opt/ericsson/nssutils/bin/node_populator create ieatnetsimv$1 >>result_ieatnetsimv$1.txt
###############################################################################################

########################## need to give input in below format################################## 
#[15:35:55 root@ieatwlvm12302:test ]# cat trigger.sh
#./script.sh 10605 &
#./script.sh 10436 &
#./script.sh 10880 &
#./script.sh 10878 &
#./script.sh 10729 &
#./script.sh 14142 &
#./script.sh 10882 &
#./script.sh 11448 &
#./script.sh 10218 &
#./script.sh 10400 &
#[15:36:25 root@ieatwlvm12302:test ]#
###################END##########################################################################