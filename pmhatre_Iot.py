import ssl
import time
import json
import random
import csv
import os
import paho.mqtt.client as mqtt
from datetime import datetime

# === AWS IoT Configuration ===
ENDPOINT = "ag9s2ws6hweux-ats.iot.us-east-2.amazonaws.com"  # e.g., a1234567xx.iot.us-east-1.amazonaws.com
PORT = 8883
CLIENT_ID = "env-station-01"
TOPIC = "environment/data"

# === Certificate File Paths ===
CA_PATH = "AmazonRootCA1.pem"
CERT_PATH = "pmhatre_IoT_inclass7.cert.pem"
KEY_PATH = "pmhatre_IoT_inclass7.private.key"

# === CSV Logging ===
CSV_FILE = "sensor_data.csv"

def generate_sensor_data():
    return {
        "station_id": CLIENT_ID,
        "temperature": round(random.uniform(-50, 50), 2),
        "humidity": round(random.uniform(0, 100), 2),
        "co2": round(random.uniform(300, 2000), 2),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "station_id", "temperature", "humidity", "co2"])
            print(f"Created new CSV file: {CSV_FILE}")

def log_to_csv(data):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            data["timestamp"],
            data["station_id"],
            data["temperature"],
            data["humidity"],
            data["co2"]
        ])

# MQTT Setup
def on_connect(client, userdata, flags, rc):
    print(f"Connected to AWS IoT Core with result code {rc}")

client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect

client.tls_set(ca_certs=CA_PATH,
               certfile=CERT_PATH,
               keyfile=KEY_PATH,
               tls_version=ssl.PROTOCOL_TLSv1_2)

client.connect(ENDPOINT, PORT)
client.loop_start()

# Start Logging
initialize_csv()

print("Publishing virtual sensor data and logging to CSV...")
try:
    while True:
        sensor_data = generate_sensor_data()
        json_payload = json.dumps(sensor_data)

        # Publish to AWS
        client.publish(TOPIC, json_payload)
        print(f"Published: {json_payload}")

        # Log locally
        log_to_csv(sensor_data)

        time.sleep(10)
except KeyboardInterrupt:
    print("\nStopped by user.")
    client.loop_stop()
