from UInterface import *
import logging

SUCCESS = 1
FAILURE	= -1

# Vending machine commands (defined below are the bitmasks used to check if the command is supported or not)
VM_SetCredit		= 0x00000001   #0
VM_GetCredit		= 0x00000002   #1
VM_ChangeCredit		= 0x00000004   #2
VM_SetInventory		= 0x00000010   #4
VM_GetInventory		= 0x00000020   #5
VM_SetInhibits		= 0x00000040   #6
VM_GetInhibits		= 0x00000080   #7
VM_SetRouting		= 0x00000100   #8
VM_GetRouting		= 0x00000200   #9
VM_NoteFloat		= 0x00000400   #10
VM_GetPositions		= 0x00000800   #11
VM_SetBezelColor	= 0x00008000   #15
VM_Payout			= 0x00010000   #16
VM_Float			= 0x00020000   #17
VM_Empty			= 0x00040000   #18
VM_NoteFloat_Payout = 0x00080000   #19
VM_NoteFloat_Stack	= 0x00100000   #20
VM_Firmware_Update	= 0x01000000   #24

#/* Vending Machine status */
STATUS_IDLE 		= 0x00
STATUS_NO_TOKEN 	= 0x01
STATUS_BUSY			= 0x40
STATUS_INIT			= 0x41
STATUS_DISPENSING	= 0x42
STATUS_FLOATING		= 0x43
STATUS_EMPTYING		= 0x44
STATUS_STACKING		= 0x45
STATUS_REJECTING	= 0x46
STATUS_READING		= 0x47
STATUS_REVALUE		= 0x48
STATUS_ERROR		= 0x80
STATUS_SILENT		= 0x81
STATUS_DEAD			= 0x82
STATUS_INCOMPPAYOUT = 0xC1
STATUS_ERRPAYOUT	= 0xC2
STATUS_INCOMPFLOAT  = 0xC3
STATUS_JAMMED		= 0xC4
STATUS_FRAUDATTEMPT	= 0xC5
STATUS_TIMEOUT		= 0xC8

#/* Interface types */
CCTALK = 0x01
ESSP   = 0x02
MDB    = 0x03
EXECUTIVE = 0x04 

#/* String formatted interface names */
interfaceName = {CCTALK : "ccTalk",
ESSP  : "eSSP",
MDB   : "MDB",
EXECUTIVE : "EXECUTIVE"}


#/* Manufacturer Codes */
UNKNOWN 			= 0x00
COMESTERO_GRP	 	= 0x01
INNOVATIVE_TECH 	= 0x02
MONEY_CONTROLS		= 0x03
RF_TECH				= 0x04
SUZO 				= 0x05 

#/* String formatted manufacturer codes */
manufacturer = {UNKNOWN : "Uknown manufacturer",
COMESTERO_GRP	 : "Comestero Group",
INNOVATIVE_TECH  : "Innovative Technology",
MONEY_CONTROLS	 : "Money Controls",
RF_TECH			 : "RF Tech",
SUZO 			 : "SUZO"}

#/* Product category codes */
PRDCT_UNKNOWN 		= 0x00
PRDCT_COIN_ACP		= 0x01
PRDCT_HOPPER		= 0x02
PRDCT_NOTE_VAL      = 0x03
PRDCT_NOTE_RCL 		= 0x04
PRDCT_CHNG_GVR 		= 0x05
PRDCT_NCSH_DEV  	= 0x06
PRDCT_NOTE_FLT		= 0x07

#/* String formatted category codes */
machineName = { PRDCT_UNKNOWN : "Unknown" ,
PRDCT_COIN_ACP	: "Coin accepter" ,
PRDCT_HOPPER	: "Hopper" ,
PRDCT_NOTE_VAL  : "Note Validator" ,
PRDCT_NOTE_RCL 	: "Note recycler" ,
PRDCT_CHNG_GVR 	: "Change giver" ,
PRDCT_NCSH_DEV  : "Cashless device" ,
PRDCT_NOTE_FLT	: "Note Float" }

#/* Currencies recognized by this module */
CURRENCY_CHF = 756 #Swiss franc Switzerland, Liechtenstein
CURRENCY_CNY = 156 #Chinese renminbi China
CURRENCY_DKK = 208 #Danish krone Denmark, Faroe Islands, Greenland
CURRENCY_EUR = 978 #Euro Andorra, Austria, Belgium, Cyprus,Estonia, Finland, France, Germany,Greece, Ireland, Italy, Kosovo,Luxembourg, Malta, Monaco,Montenegro, Netherlands, Portugal, SanMarino, Slovakia, Slovenia, Spain,Vatican City
CURRENCY_GBP = 826 #Pound sterling United Kingdom, British Crown dependencies
CURRENCY_HUF = 348 #Hungarian forint Hungary
CURRENCY_JPY = 392 #Japanese yen Japan
CURRENCY_NOK = 578 #Norwegian krone Norway
CURRENCY_PLN = 985 #Polish złoty Poland
CURRENCY_RON = 946 #Romanian new leu Romania
CURRENCY_RUB = 643 #Russian rouble Russia
CURRENCY_SEK = 752 #Swedish krona Sweden
CURRENCY_UAH = 980 #Ukrainian hryvnia Ukraine
CURRENCY_USD = 840 #United States dollar United States, various other countries
CURRENCY_TK0 = 1000 #Smart Hopper Token
CURRENCY_TK1 = 1001 #Smart Hopper Token
CURRENCY_TK2 = 1002 #Smart Hopper Token
CURRENCY_TK3 = 1003 #Smart Hopper Token
CURRENCY_TK4 = 1004 #Smart Hopper Token
CURRENCY_TK5 = 1005 #Smart Hopper Token
CURRENCY_TK6 = 1006 #Smart Hopper Token
CURRENCY_TK7 = 1007 #Smart Hopper Token
CURRENCY_TK8 = 1008 #Smart Hopper Token
CURRENCY_TK9 = 1009 #Smart Hopper Token

#/*String formatted currency names */
currencyName = {CURRENCY_CHF :"Swiss franc",
CURRENCY_CNY  :"Chinese renminbi",
CURRENCY_DKK  :"Danish krone",
CURRENCY_EUR  :"Euro",
CURRENCY_GBP  :"Pound sterling",
CURRENCY_HUF  :"Hungarian forint",
CURRENCY_JPY  :"Japanese yen",
CURRENCY_NOK  :"Norwegian krone",
CURRENCY_PLN  :"Polish złoty",
CURRENCY_RON  :"Romanian new leu",
CURRENCY_RUB  :"Russian rouble",
CURRENCY_SEK  :"Swedish krona",
CURRENCY_UAH  :"Ukrainian hryvnia",
CURRENCY_USD  :"United States dollar",
CURRENCY_TK0  :"Smart Hopper Token",
CURRENCY_TK1  :"Smart Hopper Token",
CURRENCY_TK2  :"Smart Hopper Token",
CURRENCY_TK3  :"Smart Hopper Token",
CURRENCY_TK4  :"Smart Hopper Token",
CURRENCY_TK5  :"Smart Hopper Token",
CURRENCY_TK6  :"Smart Hopper Token",
CURRENCY_TK7  :"Smart Hopper Token",
CURRENCY_TK8  :"Smart Hopper Token",
CURRENCY_TK9  :"Smart Hopper Token"}


class VendingMachine:
	def __init__(self, uinterface, index):
		self.idx = index
		self.ui  = uinterface
		self.ui.GetDeviceInfo(index)
		self.com_interface = interfaceName[self.ui.rspData["type"]]
		self.address = self.ui.rspData["address"]
		self.fab = manufacturer[self.ui.rspData["manufacturer"]]
		self.category = machineName[self.ui.rspData["category"]]
		self.nbChannels = self.ui.rspData["nbChannels"]
		self.supported_commands = self.ui.rspData["commands"]
		self.ChannelsInfo = bytearray()
		for i in range(0, self.nbChannels):
			for j in range (0,6): #Get information of the channel from the original universal interface response.
				self.ChannelsInfo.append(self.ui.rspPacket.pop(3))
		
	def refresh(self):
		self.ui.GetDeviceInfo(index)
		self.com_interface = self.ui.rspData["type"]
		self.address = self.ui.rspData["address"]
		self.fab = self.ui.rspData["manufacturer"]
		self.category = self.ui.rspData["category"]
		self.nbChannels = self.ui.rspData["nbChannels"]
		self.supported_commands = self.ui.rspData["commands"]
		self.ChannelsInfo = bytearray()
		for i in range(0, self.nbChannels):
			for j in range (0,6): #Get information of the channel from the original universal interface response.
				self.ChannelsInfo.append(self.ui.rspPacket.pop(3))
				
	def mode(self):
		return self.ui.getDeviceMode(self.idx)
	
	def status(self):
		return self.ui.getDeviceStatus(self.idx)

	def isSupported(self, command):
		return (self.supported_commands & command != 0)

	def currencyCode(self, channelID):
		tmp = self.ChannelsInfo.pop((6 * (ChannelID-1))+ 4) << 8 + self.ChannelsInfo.pop((6 * (ChannelID-1))+ 4)
		self.ChannelsInfo.insert((6 * (ChannelID-1))+ 4, tmp & 0xFF)
		self.ChannelsInfo.insert((6 * (ChannelID-1))+ 4, (tmp >> 8 )& 0xFF)
		return tmp

	def currencyName(self, channelID):
		return currencyName[self.currencyCode(channelID)]

	def setCredits(self, credit):
		if (isSupported(VND_SetCredit)):
			self.ui.setDeviceCredit(self.idx, credit)
			return SUCCESS
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def getCredits(self):
		if (isSupported(VND_GetCredit)):
			return self.ui.getDeviceCredit(self.idx)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def setInventory(self, inventory):
		if (isSupported(VM_SetInventory)):
			self.ui.setInventory(self.idx, inventory)
			return SUCCESS
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def getInventory(self):
		if (isSupported(VM_GetInventory)):
			return self.ui.getInventory(self.idx)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def EnableChannel(self, channelID):
		if (isSupported(VM_SetInhibits) & channelID <= self.nbChannels):
			temp = self.ui.GetInhibit(self.idx)
			temp = temp | (1 << (channelID -1))
			self.ui.SetInhibits(self.idx, temp)
			return SUCCESS
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def DisableChannel(self, channelID):
		if (isSupported(VM_SetInhibits) & channelID <= self.nbChannels):
			temp = self.ui.GetInhibit(self.idx)
			temp = temp & ~(1 << (channelID -1))
			self.ui.SetInhibits(self.idx, temp)
			return SUCCESS
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def isChannelEnabled(self, channelID):
		if (isSupported(VM_GetInhibits)):
			temp = self.ui.GetInhibit(self.idx)
			return (temp & (1 << (channelID - 1)) != 0)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def routeChannelToPayout(self, channelID):
		if (isSupported(VM_SetRouting) & channelID <= self.nbChannels):
			temp = self.ui.GetRouting(self.idx)
			temp = temp & ~(1 << (channelID -1))
			self.ui.SetRouting(self.idx, temp)
			return SUCCESS
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def routeChannelToCashbox(self, channelID):
		if (isSupported(VM_SetRouting) & channelID <= self.nbChannels):
			temp = self.ui.GetRouting(self.idx)
			temp = temp & ~(1 << (channelID -1))
			self.ui.SetRouting(self.idx, temp)
			return SUCCESS
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def isRoutedToPayout(self, channelID):
		if (isSupported(VM_GetRouting) & channelID <= self.nbChannels):
			temp = self.ui.GetRouting(self.idx)
			return (temp & (1 << (channelID - 1)) != 0)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def PayoutByDenomination(self, payoutAmount):
		if (isSupported(VM_Payout)):
			tmp_data = bytearray()
			tmp_data.append(self.idx)
			index = 0
			while (index < self.nbChannels) : 
				tmp_data.append(payoutAmount.pop(0))
				tmp_data.append(payoutAmount.pop(0))
				index += 1
			return self.ui.PayoutByDenomination(tmp_data)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def FloatByDenomination(self, payoutAmount):
		if (isSupported(VM_Float)):
			tmp_data = bytearray()
			tmp_data.append(self.idx)
			index = 0
			while (index < self.nbChannels) : 
				tmp_data.append(payoutAmount.pop(0))
				tmp_data.append(payoutAmount.pop(0))
				index += 1
			return self.ui.FloatByDenomination(tmp_data)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def EmptyDevice(self):
		if (isSupported(VM_Empty)):
			return self.ui.EmptyDevice(self.idx)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def ClearDeviceError(self):
		if (isSupported(VM_Empty)):
			return self.ui.ClearDeviceError(self.idx)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def GetLastPayout(self):
		return self.ui.GetLastPayout(self.idx)

	def GetTokenID(self):
		return self.ui.GetTokenID(self.idx)

	def SaveInhibits(self):
		return self.ui.SaveInhibits(self.idx)

	def SaveRouting(self):
		return self.ui.SaveRouting(self.idx)

	def ChangeChannelCredits(self, channelID, change):
		if (isSupported(VM_ChangeCredit)):
			tmp_data = bytearray()
			tmp_data.append(self.idx)
			index = 1
			while (index <= self.nbChannels) :
				if (index == channelID):
					tmp_data.append((change >> 8) & 0xFF)
					tmp_data.append(change & 0xFF)
				else:
					tmp_data.append(0)
					tmp_data.append(0)
			return self.ui.ChangeDeviceCredits(tmp_data)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def SetBezelColor(self, red, green, blue):
		if (isSupported(VM_SetBezelColor)):
			return  self.ui.SetBezelColor(self.idx, red, green, blue)
		else:
			logging.error("Command not supported by this machine")
			return FAILURE

	def GetFloatPositions(self):
		return self.ui.GetFloatPositions(self.idx)

	def DispenseLastNote(self):
		return self.ui.DispenseLastNote(self.idx)

	def StackLastNote(self):
		return self.ui.StackLastNote(self.idx)
		
