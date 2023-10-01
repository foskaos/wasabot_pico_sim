# Wasabot - "Sender"


See "Wasabot - Server". This is a client based on RPi Pico
## Phase 1
I will log sensor them in a database, and also provide a web ui to display them.

### So far I have:
* Designed a simple serial messaging protocol
* Implemented a testing environment
* Set up a raspberry pi pico to send data from a DHT-22 sensor

### Outstanding for Phase 1:
* Add light sensor


## Phase 2
Will set up various thresholds and logic to detect if environmental conditions are suitable, and actuate things to get
things in order

### Outstanding for Phase 2
* Receive Commands from server and report result
* Water pump
* Soil moisture sensor
* Fan
* Web notifications 
* Nicer web ui (graphs, responsive etc)
* Web API
