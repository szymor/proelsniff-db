#!/bin/env python3

import sys
import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("proelsniff/#")
    conn = sqlite3.connect('sniffer_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sniffer_data (
            timestamp TEXT,
            sniffer_id INTEGER,
            flat INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    if len(topic_parts) == 3 and topic_parts[2] == "flat":
        sniffer_id = topic_parts[1]
        flat_number = msg.payload.decode()
        timestamp = datetime.now().isoformat()

        conn = sqlite3.connect('sniffer_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sniffer_data (timestamp, sniffer_id, flat)
            VALUES (?, ?, ?)
        ''', (timestamp, sniffer_id, flat_number))
        conn.commit()
        conn.close()
        print(f"Stored in DB - ID: {sniffer_id}, Flat: {flat_number}")
    else:
        sniffer_id = topic_parts[1]
        subtopic = '/'.join(topic_parts[2:])
        print(f"ID: {sniffer_id}, Subtopic: {subtopic}, Message: {msg.payload.decode()}")

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
