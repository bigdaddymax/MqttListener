import paho.mqtt.client as mqtt
import mysql.connector
import os
import json
from dotenv import load_dotenv

load_dotenv()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("garage/buttons/b1")
    client.subscribe("house/stairs/sensors/s1")
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

    print(msg.topic+" "+str(msg.payload))

    if not mydb.is_connected():
        mydb.reconnect()

    sql = "INSERT INTO bell () VALUES()"
    res = cursor.execute(sql)
    mydb.commit()

def on_stairs_message(client, userdata, msg):
    """
    Message from stairs presence sensor

    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    print(msg.topic+" "+str(msg.payload))
    
    data = json.loads(msg.payload)

    if not mydb.is_connected():
        mydb.reconnect()

    sql = ("INSERT INTO motion_stairs (illumination, motion, motion_energy, presence, presence_energy) "
            "VALUES(%s, %s, %s, %s, %s)")
    res = cursor.execute(sql, (data.get('illumination'), data.get('movement'), data.get('movement_energy'), data.get('presence', 'None'), data.get('presence_energy')))
    mydb.commit()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.message_callback_add("garage/buttons/b1", on_button_message)
mqttc.message_callback_add("house/stairs/sensors/s1", on_stairs_message)

mqttc.connect("192.168.0.123", 1883, 60)

mydb = mysql.connector.connect(
    host="192.168.0.103",
    port="3307",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database="iot"
)

print('Connected to MySQL with user ' + os.getenv("MYSQL_USER"))

cursor = mydb.cursor()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()
