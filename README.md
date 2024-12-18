# Access Log System

This repository contains a system for logging and displaying events related to flats, such as door unlocking or ringing the doorbell. It consists of a script for populating a database with event data and a Flask web application for presenting this data.

## Components

### proeldb.py

`proeldb.py` is a Python script that connects to an MQTT broker to listen for events related to flats. It stores these events in an SQLite database named `accesslog.db`. The events are expected to be published under the MQTT topic format `proelsniff/<sniffer_id>/flat`, where `<sniffer_id>` is a unique identifier for the sniffer device, and the message payload contains the flat number.

#### Usage

To run the script, use the following command:

```bash
python proeldb.py <mqtt_server>
```

Replace `<mqtt_server>` with the address of your MQTT broker.

### app.py and templates

`app.py` is a Flask web application that serves a web interface to display the data collected in the `accesslog.db` database. The `templates` folder contains the HTML templates used by the Flask application.

#### Usage

To start the Flask web application, run:

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000/` by default.

## MQTT Topic Format

The MQTT topics used by this system follow the format:

```
proelsniff/<sniffer_id>/flat
```

- `<sniffer_id>`: A unique identifier for the sniffer device, which can be in hexadecimal format.
- `flat`: The subtopic indicating the event type, specifically related to flat events.

The message payload should contain the flat number associated with the event.

## Database

The SQLite database `accesslog.db` contains a table `sniffer_data` with the following columns:

- `timestamp`: The time when the event was recorded.
- `sniffer_id`: The identifier of the sniffer device.
- `flat`: The flat number associated with the event.

This setup allows for efficient logging and retrieval of flat-related events.
