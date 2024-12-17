#!/bin/env python3

import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("proelsniff/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload.decode()}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python proeldb.py <mqtt_server>")
        sys.exit(1)

    mqtt_server = sys.argv[1]

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_server, 1883, 60)

    client.loop_forever()

if __name__ == "__main__":
    main()
