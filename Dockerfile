FROM python:3.7-slim

RUN apt-get -y update
# for dlib
RUN apt-get install -y build-essential cmake
# for opencv
RUN apt-get install -y libopencv-dev

# pip install
RUN pip install paho-mqtt \
  && pip install mysql-connector-python \
    && pip install typing-extensions

COPY . .

ENTRYPOINT ["python", "script.py"]
