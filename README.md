# Garage Indicator Project

This project uses Raspberry Pi Pico W microcontrollers to read the state of a door sensor (such as a reed relay, hall effect switch, snap action switch) and wirelessly send the state of the door to an indicator node using an MQTT broker.

## Parts
1. 2x Raspberry Pi Pico W microcontrollers
2. 1x Raspberry Pi computer (or other system) with an MQTT broker installed. [See this guide for installing Mosquitto.](https://mosquitto.org/download/) You could also use a cloud-based MQTT broker.
3. WiFi network coverage.
4. 2x door sensors. These could be hall effect sensors, reed relays, or snap action switches, anything that will be able to close the connection between GND and the GPIO pin on the Pico W.
5. 3x LEDs, one each for open, closed, and changing.
6. Hookup wire
7. Solderless breadboard or perfboard.
8. Enclosure for the project

## Setting up the code
The file `indicator.py` is for the Pico with the LED output. The file `sensor.py` is for the Pico with the door sensors. The best way to do this is to upload all files to all the Picos and then add a `main.py` file with one line: either `import indicator` or `import sensor`. Each Pico will also need a `config.py` file which defines the following:

	network = "Wi-Fi network name here"
	network_password = "Wi-Fi password here"
	mqtt_server_address = "URL or IP address to MQTT broker here"

You'll need to install umqtt.simple. Do so in the Thonny REPL like this:

	import network
	import config
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	wlan.connect(config.network, config.network_password)
	import mip
	mip.install(‘umqtt.simple’)

It's possible that some firmware uses `upip` instead of `mip`.

## Installation
This is my next step.