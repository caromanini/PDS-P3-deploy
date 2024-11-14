import paho.mqtt.client as mqtt
from django.dispatch import Signal
from .signals import mqtt_message_received

"""@receiver(mqtt_message_received)
def handle_mqtt_message(sender, topic, payload, **kwargs):
    # aca va la logica
    print(f"Received MQTT message on {topic}: {payload}")"""

mqtt_message_received = Signal()

def on_connect(client, userdata, flags, rc):
    client.subscribe("Open_Locker") 


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Mensaje recibido en {msg.topic}: {payload}")
    mqtt_message_received.send(sender=client, topic=msg.topic, payload=payload)

def publish_message(topic, message):
    client.publish(topic, message)

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message



client.connect("broker.emqx.io", 1883, 60)  

client.loop_start()