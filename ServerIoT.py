import paho.mqtt.client as mqtt
import psycopg2
import json
from datetime import datetime

db_params = {
    'dbname': 'IoT_Data',
    'user': 'postgres',
    'password': 'rand123',
    'host': 'localhost',
    'port': '5432'
}

# MQTT broker settings
broker_address = "192.168.100.120"  
broker_port = 1883  

# MQTT topics to subscribe to
topics = [("test", 0), ("testSams", 0)]  

# Callback when a message is received

# def on_message(client, userdata, message):
#     print(f"Received message on topic '{message.topic}': {str(message.payload)}")

def on_message(client, userdata, message):
    # Convert the payload from bytes to a string
    payload_str = message.payload.decode('utf-8')  # Assumes UTF-8 encoding
    print(f"Received message on topic '{message.topic}': {payload_str}")
    
    try:
        payload_json = json.loads(payload_str)#parsing the JSON

        temperature = payload_json.get('temp', None)
        humidity = payload_json.get('humid', None)

        if temperature is not None and humidity is not None:
            timestamp = datetime.now()
            # #connecting and creating a cursor object in postgres
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()

            #Querry building
            sql = "INSERT INTO public.\"DHT_data\"(time, temp, humid) VALUES (%s, %s, %s)" 
            cursor.execute(sql, (timestamp, temperature, humidity))


            conn.commit()
            print(f"Data inserted temp:{temperature}, humid:{humidity} at Timestamp: {timestamp} ")
            cursor.close()
            conn.close()
        else:
            print("JSON payload does not contain 'temp' and 'humid' fields.")
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON :{str(e)}")





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
