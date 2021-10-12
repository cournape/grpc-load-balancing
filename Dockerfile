FROM python:3.9

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY client.py server.py helloworld_pb2.py helloworld_pb2_grpc.py /tmp/

WORKDIR /tmp
CMD python server.py -s 0 -l 0.05
