import sys
import os

SUCCESS = 1
FAILURE	= -1

sys.path.append(os.path.abspath("/home/oussema/uinterface"))

import UInterface
import VndMachine
import time

ui = UInterface.UnivInterface("/dev/ttyUSB0")
if (ui.getNumberOfDevices() > 0) :
	vnd = VndMachine.VendingMachine(ui, 0)
	while (vnd.status() != VndMachine.STATUS_IDLE):
		print("Waiting for the vending machine to be ready ..")
		time.sleep(1)
	print ("The vending machine connected to %s interface is a %s manufactured by %s . It has %d channels." % (vnd.com_interface, vnd.category, vnd.fab, vnd.nbChannels))
	credit = vnd.getCredits()
	for i in range(1, vnd.nbChannles+1):
		print("Credit in Channel %d : %d %s" % (i, credit.pop(0) << 8 + credit.pop(0)), vnd.currencyName(i)) #Should print something like 'Credit in Channel 2 : 14 Danish krone'
	vnd.routeChannelToCashbox(2) #Will route channel 2 to cashbox/stack
	print("Last payout is %f" % vnd.GetLastPayout())
	vnd.DisableChannel(3) #Will disable Channel 3
else:
	print ("No vending machine connected to the interface !!")
print ("Demo done !")
