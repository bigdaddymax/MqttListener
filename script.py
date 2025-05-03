import paho.mqtt.client as mqtt
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("garage/buttons/b1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_button_message(client, userdata, msg):
    """
    Messages from doorbell

    :param client:
    :param userdata:
    :param msg:
    :return:
    """

    if not mydb.is_connected():
        mydb.reconnect()

    sql = "INSERT INTO bell () VALUES()"
    res = cursor.execute(sql)
    mydb.commit()
    print(res)

def on_stairs_message(client, userdata, msg):
    """
    Message from stairs presence sensor

    :param client:
    :param userdata:
    :param msg:
    :return:
    """

    sql = "INSERT INTO "

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.message_callback_add("garage/buttons/b1", on_button_message)


mqttc.connect("192.168.0.123", 1883, 60)

mydb = mysql.connector.connect(
    host="192.168.0.103",
    port="3307",
    user=os.getenv("MYSQL_USER"),
    password="MYSQL_PASSWORD",
    database="iot"
)

cursor = mydb.cursor()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()
