FROM python:3.7-slim

ENV PYTHONUNBUFFERED=1

# pip install
RUN pip install paho-mqtt \
  && pip install mysql-connector-python \
    && pip install typing-extensions \
    && pip install python-dotenv

COPY . .

ENTRYPOINT ["python", "script.py"]
