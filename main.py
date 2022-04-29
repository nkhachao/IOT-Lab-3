import paho.mqtt.client as mqttclient
import time
import json
import serial.tools.list_ports
from process_data import processData
from constants import bbc_port, THINGS_BOARD_ACCESS_TOKEN, BROKER_ADDRESS, PORT

print("IoT Gateway")
mess = ""


if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)


def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    decoded_message = message.payload.decode("utf-8")
    temp_data = {'value': True}
    cmd = ""
    #TODO: Update the cmd to control 2 devices
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setLED":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            print('Sent', temp_data, 'to server, in response to', decoded_message)
        elif jsonobj['method'] == "setFAN":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            print('Sent', temp_data, 'to server, in response to', decoded_message)
        else:
            print('Received unsupported command', decoded_message, 'from server')
    except:
        pass

    if len(bbc_port) > 0:
        ser.write((str(cmd) + "#").encode())


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message


while True:
    if len(bbc_port) > 0:
        readSerial()

    time.sleep(1)