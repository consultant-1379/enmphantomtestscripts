# Build container
## in windows wsl ubuntu terminal
cd /mnt/c/repos/enmphantomtestscripts/hwapp
sudo mount -o loop,ro /mnt/c/Users/EEIDLE/Downloads/rhel-8.6-x86_64-dvd.iso /media/iso
sudo podman build  -f Containerfile --build-arg UID=$UID --volume=/media/iso:/media/iso:ro  -t localhost/python311_ubi:R2 .
sudo podman run --cap-add=NET_RAW -dit  --network=host -p 5000:5000  localhost/python311_ubi:R2 /bin/bash
sudo podman exec -it 62646 /bin/bash

## transfer image to webserver
sudo podman export -o R2.tar d2c7b864fbb9
sftp eeidle@atvts3202.athtem.eei.ericsson.se

## Dev env examples with volume mount of dev directory 
sudo podman run --cap-add=NET_RAW -dit --volume $PWD:/app --network=host -p 5000:5000 localhost/python311_ubi:ssl /bin/bash
--cap-add=NET_RAW is needed to the below error
[root@E-5CG2193BRF bin]# ping 192.168.0.1
bash: /usr/sbin/ping: Operation not permitted


# unity_creds = (
#     327, 12, "admin/Password123#", "5.1.2.0.5.007",
#     12, 18, "root/shRoot12!",
#     12,15, "admin/Password123!", "5.1.2.0.5.007",
#     19, "root/Password123_",
#     1, 7, 3, 18, 19, 24, 29, 25, 26, 31, 34, 36, 37, 41, 42, 43, 44, 47, 49, "admin/Password1234#",
#     27, 50, 375, "admin/Password1234_",
#     7, "localadmin/Password123_",
#     35, "admin/Password1234",
#     12, 38, "localadmin/Password1234#",
# )