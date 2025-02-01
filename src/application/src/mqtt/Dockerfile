# -------------------------------
# Target: Serial Publisher (serial_to_mqtt.py)
# -------------------------------
FROM python:3.9-slim as serial
WORKDIR /app
# Copy the serial publisher script
COPY serial_to_mqtt.py .
# Install required packages (paho-mqtt for MQTT and pyserial for serial communications)
RUN pip install --no-cache-dir paho-mqtt pyserial
# Run the serial publisher script
CMD ["python", "serial_to_mqtt.py"]

# -------------------------------
# Target: MQTT-to-API Subscriber (mqtt_to_api.py)
# -------------------------------
FROM python:3.9-slim as toapi
WORKDIR /app
# Copy the MQTT-to-API subscriber script
COPY mqtt_to_api.py .
# Install required packages (paho-mqtt for MQTT and requests for HTTP calls)
RUN pip install --no-cache-dir paho-mqtt requests
# Run the MQTT-to-API subscriber script
CMD ["python", "mqtt_to_api.py"]
