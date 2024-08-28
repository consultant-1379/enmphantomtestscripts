FROM serodocker.sero.gic.ericsson.se/proj-intive-prod/rhel7_9_extr:latest
RUN wget https://dl.dell.com/downloads/XY9D7_Navisphere-CLI-7.33.21.3.22-for-Linux-x64.rpm
RUN yum install -y XY9D7_Navisphere-CLI-7.33.21.3.22-for-Linux-x64.rpm
RUN wget https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz \ 
 && tar -xzf Python-3.9.16.tgz \
 && cd Python-3.9.16 \
 && ./configure --enable-optimizations --with-ssl \ 
 && make altinstall \
 && ln -s /usr/local/bin/python3.9 /usr/bin/python3 \
 && cd   
RUN yum install -y httpd 
RUN ln -s src/cgi-bin/enmcgi.py  /var/www/cgi-bin/enmcgi.py \
 	&&ln -s src/cgi-bin/c2.py  /var/www/cgi-bin/c2.py
#RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3.9 install --no-cache --upgrade pip setuptools
COPY requirements.txt /tmp/
RUN pip3.9 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /usr/src/myapp/src
# copy all the files to the container
COPY . /usr/src/myapp/src/
EXPOSE 80
VOLUME ["/etc/httpd/conf/httpd.conf"]
CMD ["/usr/sbin/httpd", "-DFOREGROUND"]
# docker build -t centos7_apache:1.0 -f Dockerfile .
# docker run -d -p 5000:80 --name my_apache -v /path/to/httpd/conf:/etc/httpd/conf/httpd.conf centos7_apache:1.0
