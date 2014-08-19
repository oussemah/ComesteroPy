import sys
import os

sys.path.append(os.path.abspath("/home/oussema/uinterface"))

import UInterface

SUCCESS = 1
FAILURE	= -1

ui = UInterface.UnivInterface("/dev/ttyUSB0")

ui.setRelaisClosed(0x00)

print ("Mode : "+str(ui.getMode()))

print ("Relais %d status is %d" %(0x00 , ui.getRelais(0x00)))
print ("Relais %d status is %d" %(0x01 , ui.getRelais(0x01)))
ui.setPWM(0x02, 40)
print ("PWM %d status is %d" %(0x02 , ui.getPWM(0x02)))
print ("PWM %d status is %d" %(0x01 , ui.getPWM(0x01)))

if (ui.getNumberOfIOs() != FAILURE ) :
	print ("Universal Interface has "+str(ui.rspData["relais"])+" relais, "+str(ui.rspData["pwm"])+" pwm outputs, "+str(ui.rspData["gpio"])+" io pins, from which "+str(ui.rspData["adc"])+" pins can be used as Analog Inputs and "+str(ui.rspData["dac"])+" pins can be used as Analog Outputs\n")

print ("Firmware Version : %.2f" % ui.getFirmwareVersion())

ui.wireOutputToORAndPullDown(0x05)

print("IO Config of GPIO %d is %d" % (0x05, ui.getIOConfig(0x05)))

ui.setIOHigh(0x05)
print ("IO Value of GPIO %d is %d" % (0x05, ui.getIOValue(0x05)))
ui.setIOLow(0x05)
print ("IO Value of GPIO %d is %d" % (0x05, ui.getIOValue(0x05)))

ui.calibrateADC()
print ("ADC Value of ADC%d is %d" % (0x02, ui.getADCValue(0x02)))

ui.setRelaisOpen(0x00)
print ("Relais %d status is %d" %(0x00 , ui.getRelais(0x00)))
