import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "192.168.100.120"  
broker_port = 1883  

# MQTT topics to subscribe to
topics = [("test", 0), ("Temp", 0)]  

# Callback when a message is received

# def on_message(client, userdata, message):
#     print(f"Received message on topic '{message.topic}': {str(message.payload)}")

def on_message(client, userdata, message):
    # Convert the payload from bytes to a string
    payload_str = message.payload.decode('utf-8')  # Assumes UTF-8 encoding
    print(f"Received message on topic '{message.topic}': {payload_str}")

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


client.loop_forever()