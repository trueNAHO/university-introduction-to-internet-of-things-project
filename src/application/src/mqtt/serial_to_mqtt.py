import serial
import paho.mqtt.client as mqtt

# Set up serial communication (change the port accordingly)
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust port if needed

# Set up MQTT client
mqtt_broker = "mqtt-broker"  # Change if your broker is running elsewhere
mqtt_port = 1883
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        
        if ":" in line:
            topic, value = line.rsplit(":", 1)  # Splitting from the right
            topic = topic.strip()  # Remove any whitespace
            value = value.strip()  # Remove any whitespace
            
            print(f"Publishing {value} to {topic}")
            client.publish(topic, value)
    
    except Exception as e:
        print(f"Error: {e}")

