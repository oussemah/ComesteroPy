import sys
import os

SUCCESS = 1
FAILURE	= -1

sys.path.append(os.path.abspath("/home/oussema/uinterface"))

import UInterface

ui = UInterface.UnivInterface("/dev/ttyUSB0")

print ("The interface has %d serial ports" % ui.getNumberOfSerialPorts())

ui.configSerialPort( 1, UInterface.BAUDRATE_19200, 8, UInterface.EVEN_PARITY, 1)

print ("Serial Port %d is configured as : Baudrate = %d , Parity=%d , DataBits=%d , StopBits=%d" % (1, ui.getBaudrate(1), ui.getParity(1), ui.getDataBits(1), ui.getStopBits(1)))

ui.setRTSHigh(0)
print("RTS status %d" % ui.getRTS(0))
ui.transmitViaSerial(0, b"Hello")
print("%d bytes waiting for transmission"% ui.bytesWaitingToBeTransmitted(0))
ui.setRTSLow(0)
print("%d bytes waiting to be read" % ui.bytesReceived(0))

buffer_rx = ui.read(0)
print("RX = "+buffer_rx.decode("utf-8"))
