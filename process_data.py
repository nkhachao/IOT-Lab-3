import json


def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")

    # TODO: Add your source code to publish data to the server
    json_data = {splitData[1]: splitData[2]}

    client.publish('v1/devices/me/telemetry', json.dumps(json_data), 1)
    print('Sent', json_data, 'to server, from received sensor data', splitData)