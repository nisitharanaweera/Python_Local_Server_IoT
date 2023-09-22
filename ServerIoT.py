import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "192.168.100.120"  # Replace with the IP address or hostname of your MQTT broker
broker_port = 1883  # Default MQTT port

# MQTT topics to subscribe to
topics = [("test", 0), ("Temp", 0)]  # Replace with the topics you want to subscribe to

# Callback when a message is received
def on_message(client, userdata, message):
    print(f"Received message on topic '{message.topic}': {str(message.payload)}")

# Create an MQTT client
client = mqtt.Client()

# Set the callback function for when a message is received
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Subscribe to the specified topics
for topic, qos in topics:
    client.subscribe(topic, qos=qos)
    print(f"Subscribed to topic '{topic}' with QoS {qos}")

# Start the MQTT client loop (this keeps the script running and processes messages)
client.loop_forever()
