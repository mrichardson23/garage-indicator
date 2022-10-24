# Garage Indicator Project

This project uses Raspberry Pi Pico W microcontrollers to read the state of a door sensor (such as a reed relay, hall effect switch, snap action switch) and wirelessly send the state of the door to an indicator node using an MQTT broker.

## Parts
1. 2x Raspberry Pi Pico W microcontrollers, one for the sensors and one for the indicator.
2. 1x Raspberry Pi computer (or other system) with an MQTT broker installed. [See this guide for installing Mosquitto.](https://mosquitto.org/download/) You could also use a cloud-based MQTT broker.
3. WiFi network coverage at both sensor and indicator nodes.
4. 2x door sensors. These could be hall effect sensors, reed relays, or snap action switches, anything that will be able to close the connection between GND and the GPIO pin on the Pico W. I used [these hall effect sensors](https://amzn.to/3Dt3CEU) and they worked perfectly. I 3D-printed brackets to attach these sensors to my garage.
5. 3x LEDs, green each for open, red for closed, and yellow for changing. [This is the LED assortment that I have.](https://amzn.to/3TOepi1)
6. Hookup wire. I used this [22 AWG hookup wire](https://amzn.to/3f3mGjl) for the perfboard and [this 3-conductor hookup wire](https://amzn.to/3To8tMZ) between the sensors and the project enclosure.
7. Solderless breadboard or perfboard. [This is the perfboard that I used](https://amzn.to/3F8Q4zk), but basically anything will do.
8. Enclosure for the project. [This is the one that I used for the project](https://amzn.to/3eXVOBk). Of course, even Tupperware could work, depending on the environment.

*Disclosure: The Amazon links above are affiliate links. I'll make a small commission if you buy from Amazon using that link.*

## Setting up the code
The file `indicator.py` is for the Pico with the LED output. The file `sensor.py` is for the Pico with the door sensors. The best way to do this is to upload all files to all the Picos and then add a `main.py` file with one line: either `import indicator` or `import sensor`. Each Pico will also need a `config.py` file which defines the following:

	network = "Wi-Fi network name here"
	network_password = "Wi-Fi password here"
	mqtt_server_address = "URL or IP address to MQTT broker here"

You'll need to install `umqtt.simple`. Do so in the REPL like this:

	import network
	import config
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	wlan.connect(config.network, config.network_password)
	import mip
	mip.install(‘umqtt.simple’)

*NOTE:* It's possible that your version of MicroPython for Raspberry Pi Pico uses `upip` instead of `mip`. If one does not work, simply try the other.

Feel free to add MQTT authentication to your set up if necessary. You'll need to update this:

	client = MQTTClient(client_id, mqtt_server, keepalive=0)

to this:

	client = MQTTClient(client_id, mqtt_server, keepalive=0, user="USERNAMEHERE", password="PASSWORDHERE")

in each file.

## Installation
This section is in progress.

### MQTT broker
As mentioned above, I [this guide for installing Mosquitto](https://mosquitto.org/download/). I used the same Raspberry Pi on my network that is also running my VPN server.

Most home networks use DHCP to assign IP addresses to devices. I'd recommend going into your router settings to give your MQTT broker system a DHCP reservation so that you can be sure that it always gets the same IP. This process will depend on what router you have.

I haven't tried a cloud-based MQTT broker yet.

### Sensor node

Refer to [the official Raspberry Pi Pico W pinout documentation](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf) for help with the wiring.

1. I soldered the Pico W to the perfboard so that the Wi-Fi antenna on the end is "hanging off" the edge of the perfboard. I don't want the copper in the perfboard to interfere in any way with the Wi-Fi reception.
1. I soldered two sets of 3 pin terminal blocks to the perfboard.
1. Each terminal block gets a connection to VSYS and GND to power the sensors. I soldered hookup wire for that. 
1. Each terminal block gets a connection to its own GPIO pin. As you'll see in the code, I'm using pins GP21 and GP22.
1. You can use the USB port on the Pico W for powering the project. Or solder another power connector to VSYS.
1. Mount the perfboard inside the enclosure and attach the sensors to the screw terminal blocks.
1. I used [cable glands like these](https://amzn.to/3D2b6x9) for the wire that are going out of the enclosure. 

### Indicator node

For now, the indicator node is just a Raspberry Pi Pico W with headers interted into a breadboard with LEDs on pins 16, 17, and 18.
