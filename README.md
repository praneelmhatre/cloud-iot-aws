# Cloud-Based IoT System Using MQTT

This project simulates a virtual environmental station that generates and sends sensor data (Temperature, Humidity, CO₂) to AWS IoT Core using the MQTT protocol. It also logs data locally in a CSV file.

## 📦 Features

- Virtual sensors with randomized readings
- MQTT communication via AWS IoT Core
- Local CSV data logging
- Historical data query (last 5 hours by sensor type)

## 📁 Files

- `iot_publisher_logger_csv.py` – Publishes sensor data to AWS and logs to CSV
- `query_last_5_hours.py` – Retrieves last 5 hours of data by sensor
- `sensor_data.csv` – Logged data (auto-generated)
- `certificate.pem.crt`, `private.pem.key`, `AmazonRootCA1.pem` – AWS IoT credentials (excluded from repo for security)

## 🧪 How to Run

1. Install dependencies:
   ```bash
   pip install paho-mqtt

2. Add your AWS IoT certificates and update the script with your endpoint and paths.
3. Run the script:

  python iot_publisher_logger_csv.py
