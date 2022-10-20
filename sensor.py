import network
from umqtt.simple import MQTTClient
import time
from machine import Pin
import utime
import config

openPin = Pin(21, Pin.IN, Pin.PULL_UP)
closedPin = Pin(20, Pin.IN, Pin.PULL_UP)

wlan = network.WLAN(network.STA_IF)

update_frequency = 10

wlan.active(True)
wlan.connect(config.network, config.network_password)

while not wlan.isconnected():
    pass

print("Connected to Wifi.")

mqtt_server = config.mqtt_server_address
client_id = 'Garage Pico'
topic_pub = b'garage'

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

last_time = 0
def pinHandler(pin):
    global last_time, prevState
    new_time = utime.ticks_ms()
    if (new_time - last_time > 300):
        last_time = new_time
        if pin == openPin:
            print("openPin changed.")
            if openPin.value() == 1:
                message = b'closing'
            else:
                message = b'open'
        if pin == closedPin:
            print("closedPin changed.")
            if closedPin.value() == 1:
                message = b'opening'
            else:
                message = b'closed'
        try:
            client.publish(topic_pub, message, retain=True)
        except OSError as e:
            reconnect()

openPin.irq(handler=pinHandler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
closedPin.irq(handler=pinHandler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

while True:
    if openPin.value() + closedPin.value() == 1:
        if openPin.value() == 0:
            message = b'open'
        if closedPin.value() == 0:
            message = b'closed'
        try:
            client.publish(topic_pub, message, retain=True)
        except OSError as e:
            reconnect()
    time.sleep(update_frequency)
