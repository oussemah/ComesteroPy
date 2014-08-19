ComesteroPy
===========

A python module to control the Universal Interface from Comestero Group

The Universal Interface , available at http://www.comestero-shop.de/komponenten/interface-loesungen/universal-interface/77/universal-interface, is an AVR based board that was originally built to expose different communication options between a host system (PC, RapsberryPi, BeagleBone, or any UART/USB capabale system), and different kinds of cashing/vending machines.

The firmware inside the onboard AVR implements allows routing messages between the host system and those vending machines.
But in addition to those vending machine interfaces (CCTalk, eSSP, MDB, Executive), the board provides 1 RS485 port, 1 RS232 port, up to 16 GPIOs (PWM + ADC enaled), 4 mosfet enabled outputs to drive driving up to 24V and 3.5Amps and finally 4 12V powerful Relays.

All those ports can be accessed from the host (set gpio status, read gpio status, send/recieve data through serial ports, set Relay status, read Relay status, set ADC configuration, set PWM configuration) using a high level "protocol" implemented on the firmware of the onboard AVR.

The only way to use this universal interface so far is through a java gui client allowing complete control of it (firmware update included).

The goal of this project is to provide a python module allowing easy usage of this universal interface in any python 3.0+ application.

This has been successfully tested on a Linux Mint 16 OS and on a Raspbian Wheezy OS (Most of it was tested anyway).

Please feel free to contribute or contact me at Oussema HARBI <oussema.elharbi@gmail.com>

Disclaimer :
------------
I am not currently related to Comestero Group, neither i am working for them.
I am sharing this here so that the community can profit, or may be get inspired to do something similar with other platforms.
