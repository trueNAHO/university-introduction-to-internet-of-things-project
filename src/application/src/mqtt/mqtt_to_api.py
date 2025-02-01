from datetime import datetime, timezone  # Import timezone for aware timestamps

import paho.mqtt.client as mqtt
import requests

# MQTT Broker Details
MQTT_BROKER = "mqtt-broker"  # Change if your broker is on another machine
MQTT_PORT = 1883
MQTT_TOPIC = "+/sensor/#"  # Corrected subscription filter

# API Endpoint (Replace with your actual API URL)
API_BASE_URL = "http://backend-api:8087/"  # Example API URL


# MQTT Callback - On Message Received
def on_message(client, userdata, message):
    try:
        topic_parts = message.topic.split(
            "/"
        )  # Example: ["Room1", "sensor", "Temperature"]

        if len(topic_parts) < 3:
            print(f"Invalid topic format: {message.topic}")
            return

        room_id = topic_parts[0]  # Extract Room1
        sensor = topic_parts[2]  # Extract Temperature, Light_Intensity, etc.
        value = message.payload.decode("utf-8")

        # Map the sensor to the correct field name based on the API requirements
        if sensor == "Sound":
            field_name = "sound_level"
        elif sensor == "Light_Intensity":
            field_name = "light_intensity"
        elif sensor == "Temperature":
            field_name = "temperature"
        else:
            print(f"Unknown sensor type: {sensor}")
            return

        # Construct API endpoint dynamically
        api_url = f"{API_BASE_URL}{sensor}/{room_id}"

        # Get current timezone-aware timestamp in the required format (YYYY-MM-DDTHH:MM:SS.ssssss)
        timestamp = datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )  # No timezone info

        data = {
            field_name: float(value),  # Use correct field name
            "timestamp": timestamp,  # Correct timestamp format without timezone offset
        }

        print(f"Publishing data to API: {api_url}, Data: {data}")

        # Send to API
        response = requests.post(api_url, json=data)
        if response.status_code == 201:
            print(
                f"Data stored successfully: {response.status_code}, Response: {response.text}"
            )
        else:
            print(
                f"Failed to store data: {response.status_code}, Response: {response.text}"
            )

    except Exception as e:
        print(f"Error: {e}")


# MQTT Setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to all sensor topics
client.subscribe(MQTT_TOPIC)

# Start Listening
print("Listening for MQTT messages...")
client.loop_forever()  # Ensure the client keeps running
