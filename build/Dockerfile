FROM ubuntu:17.04
RUN apt-get update && apt-get --yes install python-dev python-pip git
RUN pip install tornado requests xmltodict

RUN git clone https://github.com/hyperchi/RESTful.git

COPY config.json .
RUN mv config.json RESTful/.
CMD cd RESTful && python restful_service.py

## run command
# docker run -p 12345:12345 imagename
