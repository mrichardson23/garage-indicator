import network
import time
import config
from machine import Pin
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.network, config.network_password)

while not wlan.isconnected():
    pass

mqtt_server = config.mqtt_server_address
client_id = 'indicator'
topic_sub = b'garage'

openled = Pin(17, Pin.OUT)
closedled = Pin(16, Pin.OUT)
changingled = Pin(18, Pin.OUT)

def mqtt_event(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "open":
        closedled.value(0)
        changingled.value(0)
        openled.value(1)
    if msg == "closed":
        closedled.value(1)
        changingled.value(0)
        openled.value(0)
    if msg == "closing":
        closedled.value(0)
        changingled.value(1)
        openled.value(0)
    if msg == "opening":
        closedled.value(0)
        changingled.value(1)
        openled.value(0)
    
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=0)
    client.set_callback(mqtt_event)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
    

client.subscribe(topic_sub)

while True:
    try:
        print("waiting for message...")
        client.wait_msg()
    except OSError as e:
        reconnect()