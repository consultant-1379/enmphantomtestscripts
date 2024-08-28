FROM registry.access.redhat.com/ubi8/ubi-minimal
RUN microdnf install -y python3
WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install --upgrade pip
RUN python3 -m pip install -r /app/requirements.txt
EXPOSE 5000
COPY ./*.py /app
COPY ./data /app
COPY ./tests /app
RUN mkdir /app/logs
CMD ["saninfo.py"]
