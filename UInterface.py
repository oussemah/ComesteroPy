# Command Packet format  : LEN ID CMD-G CMD-S DATA CRC

# Response Packet Format : LEN ID RES DATA CRC

from serial import Serial
from crc16custom import _crc16
import binascii
import os
import logging
import struct
import time
import numpy

BAUDRATE = 115200
TIMEOUT  = 2

SUCCESS = 1
FAILURE	= -1


#/* Response Codes */
RSP_OK 			= 0xF0
RSP_UKNOWNCMD 	= 0xF1
RSP_NSUPPORTED	= 0xF2
RSP_BADPRMNUMB 	= 0xF3
RSP_OUTOFRANGE  = 0xF4
RSP_ERRPROCESS 	= 0xF5
RSP_DEVSOFTERR 	= 0xF6
RSP_CRCERROR	= 0xF7

#/** System Commands : GRP 0x01 **/
CMD_SYSTEM_Reset			= 0x0100
CMD_SYSTEM_EnterBootloader  = 0x0101
CMD_SYSTEM_ExitBootloader 	= 0x0102
CMD_SYSTEM_GetMode 			= 0x0103
CMD_SYSTEM_ProgramFlash 	= 0x0104
CMD_SYSTEM_ProgramEEPROM 	= 0x0105
CMD_SYSTEM_GetFirmwareVersion 		= 0x0106 

#/** IO Commands : GRP 0x02 **/
CMD_IO_GetNumberOfIOs 		= 0x0200
CMD_IO_ADCCalibration 		= 0x0201
CMD_IO_SetRelais 		= 0x0202	# Relais ID (1 byte) 	State (1 byte)
CMD_IO_GetRelais 		= 0x0203	# Relais ID (1 byte)
CMD_IO_SetPWM 			= 0x0204	# PWM ID (1 byte) 		Value (1 byte)
CMD_IO_GetPWM 			= 0x0205	# PWM ID (1 byte)
CMD_IO_SetIOConfig 		= 0x0206	# IO ID (1 byte) 		Config (1 byte)
CMD_IO_GetIOConfig 		= 0x0207	# IO ID (1 byte)
CMD_IO_SetIoValue 		= 0x0208	# IO ID (1 byte) 		Value (1 byte)
CMD_IO_GetIoValue 		= 0x0209	# IO ID (1 byte)
CMD_IO_GetADCValue 		= 0x020A	# IO ID (1 byte)

#/** Serial Commands GRP: 0x03 **/
CMD_SER_GetNumberOfSerialPorts 			= 0x0300
CMD_SER_SetBaudrate 				= 0x0301	# Serial ID (1 byte) Value (1 byte)
CMD_SER_GetBaudrate 				= 0x0302	# Serial ID (1 byte)
CMD_SER_SetDatabits 				= 0x0303	# Serial ID (1 byte) Value (1byte)
CMD_SER_GetDatabits 				= 0x0304	# Serial ID (1 byte)
CMD_SER_SetParity 				= 0x0305	# Serial ID (1 byte) Value (1 byte)
CMD_SER_GetParity 				= 0x0306	# Serial ID (1 byte)
CMD_SER_SetStopbits 				= 0x0307	# Serial ID (1 byte) Value (1byte)
CMD_SER_GetStopbits 				= 0x0308	# Serial ID (1 byte)
CMD_SER_Transmit 				= 0x0309	# Serial ID (1 byte) Data (1-120bytes)
CMD_SER_GetBytesInTxBuffer 			= 0x030A	# Serial ID (1 byte)
CMD_SER_Receive 				= 0x030B	# Serial ID (1 byte)
CMD_SER_GetBytesInRxBuffer 			= 0x030C	# Serial ID (1 byte)
CMD_SER_ReceiveAndClear 			= 0x030D	# Serial ID (1 byte)
CMD_SER_SetDTR 					= 0x030E	# Serial ID (1 byte) State (1 byte)
CMD_SER_GetDTR 					= 0x030F	# Serial ID (1 byte)
CMD_SER_SetRTS 					= 0x0310	# Serial ID (1 byte) State (1 byte)
CMD_SER_GetRTS 					= 0x0311	# Serial ID (1 byte)
CMD_SER_GetDSR 					= 0x0312	# Serial ID (1 byte)
CMD_SER_GetCTS 					= 0x0313	# Serial ID (1 byte) 

#/** Vending Interface Commands GRP: 0x04 **/
CMD_VND_GetNumberOfDevices 		= 0x0400 
CMD_VND_GetDeviceInfo 			= 0x0401 	# ID (1 byte)
CMD_VND_SetDeviceMode 			= 0x0402	# ID (1 byte) Mode (1 byte)
CMD_VND_GetDeviceMode 			= 0x0403	# ID (1 byte)
CMD_VND_GetDeviceStatus 		= 0x0404	# ID (1 byte)
CMD_VND_SetDeviceCredit 		= 0x0405	# ID (1 byte) Value (4 bytes)
CMD_VND_GetDeviceCredit 		= 0x0406	# ID (1 byte)
CMD_VND_SetInventory 			= 0x0407	# ID (1 byte) Values (n * 2 bytes)
CMD_VND_GetInventory 			= 0x0408	# ID (1 byte)
CMD_VND_SetInhibits 			= 0x0409	# ID (1 byte) Values (2 bytes)
CMD_VND_GetInhibits 			= 0x040A	# ID (1 byte)
CMD_VND_SetRouting 				= 0x040B	# ID (1 byte) Values (2 bytes)
CMD_VND_GetRouting 				= 0x040C	# ID (1 byte)
CMD_VND_PayoutByDenomination	= 0x040D	# ID (1 byte) Values (n * 2 bytes)
CMD_VND_FloatByDenomination 	= 0x040E	# ID (1 byte) Values (n * 2 bytes)
CMD_VND_EmptyDevice 			= 0x040F	# ID (1 byte)
CMD_VND_ClearDeviceErrorStatus 	= 0x0410	# ID (1 byte)
CMD_VND_GetLastPayout 			= 0x0411	# ID (1 byte)
CMD_VND_GetTokenID 				= 0x0412	# ID (1 byte)
CMD_VND_ChangeCredit 			= 0x0413	# ID (1 byte) Value (4 bytes)
CMD_VND_SetBezelColor 			= 0x0414	# ID (1 byte) RGB (3 Bytes)
CMD_VND_NoteFloatGetPositions   = 0x0415	# ID (1 byte)
CMD_VND_NoteFloatPayout			= 0x0416	# ID (1 byte)
CMD_VND_NoteFloatToStacker		= 0x0417	# ID (1 byte)
CMD_VND_SaveInhibits 			= 0x0419	# ID (1 byte)
CMD_VND_SaveRoutings 			= 0x041B	# ID (1 byte)

#/* IO Configuration */
IO_CONFIG_FLOAT 				= 0x00 
IO_CONFIG_KEEP 					= 0x01 
IO_CONFIG_PULLL_DOWN			= 0x02
IO_CONFIG_PULL_UP				= 0x03
IO_CONFIG_FLOAT_INVERTED		= 0x08
IO_CONFIG_KEEP_INVERTED			= 0x09
IO_CONFIG_PULL_DOWN_INVERTED	= 0x0A
IO_CONFIG_PULL_UP_INVERTED		= 0x0B
IO_CONFIG_PUSH_PULL 					= 0x20
IO_CONFIG_WIRED_OR 						= 0x24
IO_CONFIG_WIRED_AND						= 0x25
IO_CONFIG_WIRED_OR_PULL_DOWN			= 0x26
IO_CONFIG_WIRED_AND_PULL_UP				= 0x27
IO_CONFIG_PUSH_PULL_INVERTED			= 0x28
IO_CONFIG_WIRED_OR_INVERTED				= 0x2C
IO_CONFIG_WIRED_AND_INVERTED			= 0x2D
IO_CONFIG_WIRED_OR_PULL_DOWN_INVERTED 	= 0x2E
IO_CONFIG_WIRED_AND_PULL_UP_INVERTED	= 0x2F

#/* Baudrate values */
BAUDRATE_300 	= 0x00
BAUDRATE_600 	= 0x01
BAUDRATE_1200 	= 0x02
BAUDRATE_2400 	= 0x03
BAUDRATE_4800 	= 0x04
BAUDRATE_9600 	= 0x05
BAUDRATE_14400 	= 0x06
BAUDRATE_19200 	= 0x07
BAUDRATE_28800 	= 0x08
BAUDRATE_38400 	= 0x09
BAUDRATE_56000 	= 0x0A
BAUDRATE_57600 	= 0x0B
BAUDRATE_115200 = 0x0C
BAUDRATE_128000 = 0x0D
BAUDRATE_256000 = 0x0E

#/* Partiy Config */
NO_PARITY  	= 0x00
ODD_PARITY 	= 0x01
EVEN_PARITY	= 0x02

#/* data size of each command */
dataSize= {CMD_SYSTEM_Reset : 0,
CMD_SYSTEM_EnterBootloader : 0,
CMD_SYSTEM_ExitBootloader : 0,
CMD_SYSTEM_GetMode : 0,
CMD_SYSTEM_ProgramFlash : 0,
CMD_SYSTEM_ProgramEEPROM : 0,
CMD_SYSTEM_GetFirmwareVersion : 0,
CMD_IO_GetNumberOfIOs : 0,
CMD_IO_ADCCalibration : 0,
CMD_IO_SetRelais : 2,
CMD_IO_GetRelais : 1,
CMD_IO_SetPWM : 2,
CMD_IO_GetPWM : 1,
CMD_IO_SetIOConfig : 2,
CMD_IO_GetIOConfig : 1,
CMD_IO_SetIoValue : 2,
CMD_IO_GetIoValue : 1,
CMD_IO_GetADCValue : 1,
CMD_SER_GetNumberOfSerialPorts : 0,
CMD_SER_SetBaudrate : 2,
CMD_SER_GetBaudrate : 1,
CMD_SER_SetDatabits : 2,
CMD_SER_GetDatabits : 1,
CMD_SER_SetParity : 2,
CMD_SER_GetParity : 1,
CMD_SER_SetStopbits : 2,
CMD_SER_GetStopbits : 1,
CMD_SER_Transmit : 1,
CMD_SER_GetBytesInTxBuffer : 1,
CMD_SER_Receive : 1,
CMD_SER_GetBytesInRxBuffer : 1,
CMD_SER_ReceiveAndClear : 1,
CMD_SER_SetDTR : 2,
CMD_SER_GetDTR : 1,
CMD_SER_SetRTS : 2,
CMD_SER_GetRTS : 1,
CMD_SER_GetDSR : 1,
CMD_SER_GetCTS : 1,
CMD_VND_GetNumberOfDevices : 0,
CMD_VND_GetDeviceInfo : 1,
CMD_VND_SetDeviceMode : 2,
CMD_VND_GetDeviceMode : 1,
CMD_VND_GetDeviceStatus : 1,
CMD_VND_SetDeviceCredit : 2,
CMD_VND_GetDeviceCredit : 1,
CMD_VND_SetInventory : 2,
CMD_VND_GetInventory : 1,
CMD_VND_SetInhibits : 2,
CMD_VND_GetInhibits : 6,
CMD_VND_SetRouting : 2,
CMD_VND_GetRouting : 1,
CMD_VND_PayoutByDenomination : 1,
CMD_VND_FloatByDenomination : 1,
CMD_VND_EmptyDevice : 1,
CMD_VND_ClearDeviceErrorStatus : 1,
CMD_VND_GetLastPayout : 1,
CMD_VND_GetTokenID : 1,
CMD_VND_ChangeCredit : 5,
CMD_VND_SetBezelColor : 4,
CMD_VND_NoteFloatGetPositions : 1,
CMD_VND_NoteFloatPayout : 1,
CMD_VND_NoteFloatToStacker : 1,
CMD_VND_SaveInhibits : 1,
CMD_VND_SaveRoutings : 1}

rspSize= {CMD_SYSTEM_Reset : 4,
CMD_SYSTEM_EnterBootloader : 4,
CMD_SYSTEM_ExitBootloader : 4,
CMD_SYSTEM_GetMode : 5,
CMD_SYSTEM_ProgramFlash : 4,
CMD_SYSTEM_ProgramEEPROM : 4,
CMD_SYSTEM_GetFirmwareVersion : 6,
CMD_IO_GetNumberOfIOs : 9,
CMD_IO_ADCCalibration : 4,
CMD_IO_SetRelais : 4,
CMD_IO_GetRelais : 5,
CMD_IO_SetPWM : 4,
CMD_IO_GetPWM : 5,
CMD_IO_SetIOConfig : 4,
CMD_IO_GetIOConfig : 5,
CMD_IO_SetIoValue : 4,
CMD_IO_GetIoValue : 6,
CMD_IO_GetADCValue : 6,
CMD_SER_GetNumberOfSerialPorts : 5,
CMD_SER_SetBaudrate : 4,
CMD_SER_GetBaudrate : 5,
CMD_SER_SetDatabits : 4,
CMD_SER_GetDatabits : 5,
CMD_SER_SetParity : 4,
CMD_SER_GetParity : 5,
CMD_SER_SetStopbits : 4,
CMD_SER_GetStopbits : 5,
CMD_SER_Transmit : 0,
CMD_SER_GetBytesInTxBuffer : 5,
CMD_SER_Receive : 0,
CMD_SER_GetBytesInRxBuffer : 5,
CMD_SER_ReceiveAndClear : 0,
CMD_SER_SetDTR : 4,
CMD_SER_GetDTR : 5,
CMD_SER_SetRTS : 4,
CMD_SER_GetRTS : 5,
CMD_SER_GetDSR : 5,
CMD_SER_GetCTS : 5,
CMD_VND_GetNumberOfDevices : 5,
CMD_VND_GetDeviceInfo : 0, #We calculate that dynamically
CMD_VND_SetDeviceMode : 4,
CMD_VND_GetDeviceMode : 5,
CMD_VND_GetDeviceStatus : 5,
CMD_VND_SetDeviceCredit : 4,
CMD_VND_GetDeviceCredit : 0, # depends on channel number
CMD_VND_SetInventory : 4,
CMD_VND_GetInventory : 0,
CMD_VND_SetInhibits : 4,
CMD_VND_GetInhibits : 6,
CMD_VND_SetRouting : 4,
CMD_VND_GetRouting : 6,
CMD_VND_PayoutByDenomination : 4,
CMD_VND_FloatByDenomination : 4,
CMD_VND_EmptyDevice : 4,
CMD_VND_ClearDeviceErrorStatus : 4,
CMD_VND_GetLastPayout : 0,
CMD_VND_GetTokenID : 8,
CMD_VND_ChangeCredit : 4,
CMD_VND_SetBezelColor : 4,
CMD_VND_NoteFloatGetPositions : 1,
CMD_VND_NoteFloatPayout : 4,
CMD_VND_NoteFloatToStacker : 4,
CMD_VND_SaveInhibits : 1,
CMD_VND_SaveRoutings : 1}

#/* string format of commands "#/*",
commandToString ={ CMD_SYSTEM_Reset : "CMD_SYSTEM_Reset",
CMD_SYSTEM_EnterBootloader : "CMD_SYSTEM_EnterBootloader",
CMD_SYSTEM_ExitBootloader : "CMD_SYSTEM_ExitBootloader",
CMD_SYSTEM_GetMode : "CMD_SYSTEM_GetMode",
CMD_SYSTEM_ProgramFlash : "CMD_SYSTEM_ProgramFlash",
CMD_SYSTEM_ProgramEEPROM : "CMD_SYSTEM_ProgramEEPROM",
CMD_SYSTEM_GetFirmwareVersion : "CMD_SYSTEM_GetFirmwareVersion",
CMD_IO_GetNumberOfIOs : "CMD_IO_GetNumberOfIOs",
CMD_IO_ADCCalibration : "CMD_IO_ADCCalibration",
CMD_IO_SetRelais : "CMD_IO_SetRelais",
CMD_IO_GetRelais : "CMD_IO_GetRelais",
CMD_IO_SetPWM : "CMD_IO_SetPWM",
CMD_IO_GetPWM : "CMD_IO_GetPWM",
CMD_IO_SetIOConfig : "CMD_IO_SetIOConfig",
CMD_IO_GetIOConfig : "CMD_IO_GetIOConfig",
CMD_IO_SetIoValue : "CMD_IO_SetIoValue",
CMD_IO_GetIoValue : "CMD_IO_GetIoValue",
CMD_IO_GetADCValue : "CMD_IO_GetADCValue",
CMD_SER_GetNumberOfSerialPorts : "CMD_SER_GetNumberOfSerialPorts",
CMD_SER_SetBaudrate : "CMD_SER_SetBaudrate",
CMD_SER_GetBaudrate : "CMD_SER_GetBaudrate",
CMD_SER_SetDatabits : "CMD_SER_SetDatabits",
CMD_SER_GetDatabits : "CMD_SER_GetDatabits",
CMD_SER_SetParity : "CMD_SER_SetParity",
CMD_SER_GetParity : "CMD_SER_GetParity",
CMD_SER_SetStopbits : "CMD_SER_SetStopbits",
CMD_SER_GetStopbits : "CMD_SER_GetStopbits",
CMD_SER_Transmit : "CMD_SER_Transmit",
CMD_SER_GetBytesInTxBuffer : "CMD_SER_GetBytesInTxBuffer",
CMD_SER_Receive : "CMD_SER_Receive",
CMD_SER_GetBytesInRxBuffer : "CMD_SER_GetBytesInRxBuffer",
CMD_SER_ReceiveAndClear : "CMD_SER_ReceiveAndClear",
CMD_SER_SetDTR : "CMD_SER_SetDTR",
CMD_SER_GetDTR : "CMD_SER_GetDTR",
CMD_SER_SetRTS : "CMD_SER_SetRTS",
CMD_SER_GetRTS : "CMD_SER_GetRTS",
CMD_SER_GetDSR : "CMD_SER_GetDSR",
CMD_SER_GetCTS : "CMD_SER_GetCTS",
CMD_VND_GetNumberOfDevices : "CMD_VND_GetNumberOfDevices",
CMD_VND_GetDeviceInfo : "CMD_VND_GetDeviceInfo",
CMD_VND_SetDeviceMode : "CMD_VND_SetDeviceMode",
CMD_VND_GetDeviceMode : "CMD_VND_GetDeviceMode",
CMD_VND_GetDeviceStatus : "CMD_VND_GetDeviceStatus",
CMD_VND_SetDeviceCredit : "CMD_VND_SetDeviceCredit",
CMD_VND_GetDeviceCredit : "CMD_VND_GetDeviceCredit",
CMD_VND_SetInventory : "CMD_VND_SetInventory",
CMD_VND_GetInventory : "CMD_VND_GetInventory",
CMD_VND_SetInhibits : "CMD_VND_SetInhibits",
CMD_VND_GetInhibits : "CMD_VND_GetInhibits",
CMD_VND_SetRouting : "CMD_VND_SetRouting",
CMD_VND_GetRouting : "CMD_VND_GetRouting",
CMD_VND_PayoutByDenomination : "CMD_VND_PayoutByDenomination",
CMD_VND_FloatByDenomination : "CMD_VND_FloatByDenomination",
CMD_VND_EmptyDevice : "CMD_VND_EmptyDevice",
CMD_VND_ClearDeviceErrorStatus : "CMD_VND_ClearDeviceErrorStatus",
CMD_VND_GetLastPayout : "CMD_VND_GetLastPayout",
CMD_VND_GetTokenID : "CMD_VND_GetTokenID",
CMD_VND_ChangeCredit : "CMD_VND_ChangeCredit",
CMD_VND_SetBezelColor : "CMD_VND_SetBezelColor",
CMD_VND_SaveInhibits : "CMD_VND_SaveInhibits",
CMD_VND_SaveRoutings : "CMD_VND_SaveRoutings",
CMD_VND_NoteFloatGetPositions : "CMD_VND_NoteFloatGetPositions",
CMD_VND_NoteFloatPayout : "CMD_VND_NoteFloatPayout",
CMD_VND_NoteFloatToStacker : "CMD_VND_NoteFloatToStacker"}

DATA_NONE = bytearray()

def crc16(commandPacket):
	return _crc16(commandPacket)

class UnivInterface :
	def __init__(self, portName):
		self.currentMsgID = 0
		self.rspData = {}
		self.cmdPacket = bytearray()
		self.rspPacket = bytearray()
		self.serialPort = Serial( portName, baudrate=BAUDRATE, timeout=None); # ALL other params are as default values
		if (self.serialPort.isOpen() == False):
			self.serialPort.open()
		self.serialPort.flushInput()
		self.serialPort.flushOutput()

	def sendCommand(self, command, data=DATA_NONE, forceID=b'\x00'):
		self.cmdPacket = bytearray()
		self.cmdPacket.append(dataSize[command] + 5)
		if (forceID != b'\x00'):
			self.cmdPacket.append(forceID)
		else:
			self.cmdPacket.append(self.currentMsgID)
		self.cmdPacket.append((command >> 8)& 0xFF)
		self.cmdPacket.append(command & 0xFF)
		for i in range (0, dataSize[command]):
			self.cmdPacket.append(data[i])
		rawCrc = crc16(self.cmdPacket)
		self.cmdPacket.append( rawCrc & 0xFF)
		self.cmdPacket.append( (rawCrc >> 8) & 0xFF)
		logging.debug ("Sending command b'"+binascii.hexlify(self.cmdPacket).decode("utf-8")+"'")		
		self.currentMsgID+=1
		self.serialPort.write(self.cmdPacket)
		time.sleep(1)

	def getResponse(self, command):
		a = 0
		self.rspPacket = bytearray()
		while ( self.serialPort.inWaiting() > 0 ):	
			self.rspPacket.append(self.serialPort.read(1)[0])
			a += 1
		if a < 1:
			logging.error("No Response Recieved")
			return FAILURE
		size = self.rspPacket.pop(0)
		if  size != rspSize[command] :
			if rspSize[command] != 0 :
				logging.error(commandToString[command]+ " : Response Message is not the correct size " +str(size) + " instead of "+ str(rspSize[command]) + " : 0x"+":0x".join("{:02x}".format(c) for c in self.rspPacket))
				return FAILURE
		self.rspPacket.insert(0, size)
		msgid = self.rspPacket.pop(1)
		if msgid != (self.currentMsgID - 1):
			logging.error(commandToString[command]+ " : Bad Message ID "+str(msgid)+" instead of "+str(self.currentMsgID - 1) + " : 0x"+":0x".join("{:02x}".format(c) for c in self.rspPacket))
			return FAILURE
		self.rspPacket.insert(1, msgid)
		rspCode = self.rspPacket.pop(2)
		if rspCode != RSP_OK :
			logging.error(commandToString[command]+ " : Interface Response is not OK : "+str(rspCode) + " : 0x"+":0x".join("{:02x}".format(c) for c in self.rspPacket))
			return FAILURE
		self.rspPacket.insert(2, rspCode)
		msgCRC = (self.rspPacket.pop(-1) << 8) + self.rspPacket.pop(-1)
		if crc16(self.rspPacket) != msgCRC :
			logging.error(commandToString[command]+ " : Bad CRC for the recieved response " + str(crc16(self.rspPacket)) + " !=  "+ str(msgCRC) + " : 0x"+":0x".join("{:02x}".format(c) for c in self.rspPacket))
			return FAILURE
		else:
			self.rspPacket.append(msgCRC & 0xFF)
			self.rspPacket.append((msgCRC >> 8 ) & 0xFF)
			logging.debug(commandToString[command]+ " : Response : 0x"+":0x".join("{:02x}".format(c) for c in self.rspPacket))
		return SUCCESS

	def decodeResponse(self,command):
		if self.getResponse(command) != SUCCESS :
			return FAILURE
		if command == CMD_SYSTEM_GetMode :
			mode = self.rspPacket.pop(3)
			return mode
		elif command == CMD_SYSTEM_GetFirmwareVersion :
			version_temp = bytearray()
			version_temp.append(self.rspPacket.pop(3))
			version_temp.insert(0, self.rspPacket.pop(3))
			version=numpy.frombuffer(version_temp, dtype=numpy.float16)[0]
			return version * 100000
		elif command == CMD_IO_GetNumberOfIOs :
			self.rspData = { "relais" : self.rspPacket.pop(3), "pwm" : self.rspPacket.pop(3), "gpio" : self.rspPacket.pop(3), "adc" : self.rspPacket.pop(3), "dac" : self.rspPacket.pop(3)}
			return self.rspData
		elif command == CMD_IO_GetRelais :
			status = self.rspPacket.pop(3)
			return status
		elif command == CMD_IO_GetPWM :
			dutyCycle = (self.rspPacket.pop(3) * 100 ) // 255
			return dutyCycle
		elif command == CMD_IO_GetIOConfig :
			config = self.rspPacket.pop(3)
			return config
		elif command == CMD_IO_GetIoValue :
			value = self.rspPacket.pop(3)
			return value
		elif command == CMD_IO_GetADCValue :
			value = self.rspPacket.pop(3) + (self.rspPacket.pop(3) << 8)
			return value
		elif command == CMD_SER_GetNumberOfSerialPorts :
			nb = self.rspPacket.pop(3)
			return nb
		elif command == CMD_SER_GetBaudrate :
			baudrate = self.rspPacket.pop(3)
			return baudrate
		elif command == CMD_SER_GetParity :
			parity = self.rspPacket.pop(3)
			return parity
		elif command == CMD_SER_GetStopbits :
			stopbits = self.rspPacket.pop(3)
			return stopbits
		elif command == CMD_SER_GetBytesInTxBuffer :
			nb = self.rspPacket.pop(3)
			return nb
		elif command == CMD_SER_GetBytesInRxBuffer :
			nb = self.rspPacket.pop(3)
			return nb
		elif command == CMD_SER_GetDatabits :
			databits = self.rspPacket.pop(3)
			return databits
		elif command == CMD_SER_GetDTR :
			dtrStatus = self.rspPacket.pop(3)
			return dtrStatus
		elif command == CMD_SER_GetRTS :
			rtsStatus = self.rspPacket.pop(3)
			return rtsStatus
		elif command == CMD_SER_GetDSR :
			dsrStatus = self.rspPacket.pop(3)
			return dsrStatus
		elif command == CMD_SER_GetCTS :
			ctsStatus = self.rspPacket.pop(3)
			return ctsStatus
		elif command == CMD_SER_Receive or command == CMD_SER_ReceiveAndClear:
			self.serialBuffer = bytearray()
			size = self.rspPacket.pop(0)
			self.rspPacket.insert(0, size)
			for i in range(0, size-4) :
				self.serialBuffer.append(self.rspPacket.pop(3)) 
			return self.serialBuffer
		elif command == CMD_VND_GetNumberOfDevices :
			nb = self.rspPacket.pop(3)
			return nb
		elif command == CMD_VND_GetDeviceInfo :
			self.rspData = {"type" : self.rspPacket.pop(3), "address" : self.rspPacket.pop(3), "manufacturer" : self.rspPacket.pop(3), "category" : self.rspPacket.pop(3), "nbChannels" : self.rspPacket.pop(3), "commands" : self.rspPacket.pop(-3)+(self.rspPacket.pop(-3) << 8)+(self.rspPacket.pop(-3) << 16)+(self.rspPacket.pop(-3) << 24)}
			return rspData
		elif command == CMD_VND_GetDeviceMode :
			mode = self.rspPacket.pop(3)
			return mode
		elif command == CMD_VND_GetDeviceStatus :
			status = self.rspPacket.pop(3)
			return status
		elif command == CMD_VND_GetDeviceCredit :
			credit = bytearray()
			size = self.rspPacket.pop(0)
			self.rspPacket.insert(0, size)
			for i in range(0,  size-4):
				credit.append(self.rspPacket.pop(3))
			return credit
		elif command == CMD_VND_GetInventory :
			inventory = bytearray()
			size = self.rspPacket.pop(0)
			self.rspPacket.insert(0, size)
			for i in range(0,  size-4):
				inventory.append(self.rspPacket.pop(3))
			return inventory
		elif command == CMD_VND_GetInhibits :
			inhibits = (self.rspPacket.pop(3) << 8) + self.rspPacket.pop(3)
			return inhibits
		elif command == CMD_VND_GetRouting :
			routing = (self.rspPacket.pop(3) << 8) + self.rspPacket.pop(3)
			return routing
		elif command == CMD_VND_GetLastPayout :
			payout_temp = bytearray()
			payout_temp.append(self.rspPacket.pop(3))
			payout_temp.insert(0, self.rspPacket.pop(3))
			payout=numpy.frombuffer(payout_temp, dtype=numpy.float16)[0]
			return payout
		elif command == CMD_VND_GetTokenID :
			tokenid = self.rspPacket.pop(3) + (self.rspPacket.pop(3) << 8) + (self.rspPacket.pop(3) << 16) + (self.rspPacket.pop(3) << 24)
			return tokenid
		elif command == CMD_VND_NoteFloatGetPositions :
			return
		else:
			return SUCCESS

	def reset(self):
		self.sendCommand(CMD_SYSTEM_Reset)
		return self.decodeResponse(CMD_SYSTEM_Reset)
		
	def enterBootLoaderMode(self):
		self.sendCommand(CMD_SYSTEM_EnterBootloader)
		return self.decodeResponse(CMD_SYSTEM_EnterBootloader)

	def exitBootLoaderMode(self):
		self.sendCommand(CMD_SYSTEM_ExitBootloader)
		return self.decodeResponse(CMD_SYSTEM_ExitBootloader)

	def getMode(self):
		self.sendCommand(CMD_SYSTEM_GetMode)
		return self.decodeResponse(CMD_SYSTEM_GetMode)

	def programFlash(self, filePath):
		statinfo = os.stat(filePath)
		self.sendCommand(CMD_SYSTEM_ProgramFlash, statinfo.st_size)
		fd = open(filePath, "rb")
		for i in range(0, statinfo.st_size):
			self.serialPort.write(fd.read(1))
		#check if response is OK
		return self.decodeResponse(CMD_SYSTEM_ProgramFlash)
	
	def programEEPROM(self, filePath):
		statinfo = os.stat(filePath)
		self.sendCommand(CMD_SYSTEM_ProgramEEPROM, statinfo.st_size)
		fd = open(filePath, "rb")
		for i in range(0, statinfo.st_size):
			self.serialPort.write(fd.read(1))
		#check if response is OK
		return self.decodeResponse(CMD_SYSTEM_ProgramEEPROM)

	def getFirmwareVersion(self):
		self.sendCommand(CMD_SYSTEM_GetFirmwareVersion)
		return self.decodeResponse(CMD_SYSTEM_GetFirmwareVersion)

	def getNumberOfIOs(self):
		self.sendCommand(CMD_IO_GetNumberOfIOs)
		return self.decodeResponse(CMD_IO_GetNumberOfIOs)

	def calibrateADC(self):
		self.sendCommand(CMD_IO_ADCCalibration)
		return self.decodeResponse(CMD_IO_ADCCalibration)

	def setRelaisClosed(self, relaisID):
		tmp_data = bytearray()
		tmp_data.append(relaisID)
		tmp_data.append(0x01)
		self.sendCommand(CMD_IO_SetRelais, tmp_data)
		return self.decodeResponse(CMD_IO_SetRelais)

	def setRelaisOpen(self, relaisID):
		tmp_data = bytearray()
		tmp_data.append(relaisID)
		tmp_data.append(0x00)
		self.sendCommand(CMD_IO_SetRelais, tmp_data)
		return self.decodeResponse(CMD_IO_SetRelais)

	def getRelais(self, relaisID):
		tmp_data = bytearray()
		tmp_data.append(relaisID)
		self.sendCommand(CMD_IO_GetRelais, tmp_data)
		return self.decodeResponse(CMD_IO_GetRelais)

	def setPWM(self, pwmID, pwmValue):
		tmp_data = bytearray()
		tmp_data.append(pwmID)
		tmp_data.append((pwmValue * 255 ) // 100)
		self.sendCommand(CMD_IO_SetPWM, tmp_data)
		return self.decodeResponse(CMD_IO_SetPWM)

	def getPWM(self, pwmID):
		tmp_data = bytearray()
		tmp_data.append(pwmID)
		self.sendCommand(CMD_IO_GetPWM, tmp_data)
		return self.decodeResponse(CMD_IO_GetPWM)

	def setInputFloating(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_FLOAT)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def keepIOStatusConfig(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_KEEP)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def pullDownInput(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_PULLL_DOWN)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def pullUpInput(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_PULL_UP)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def setInputFloatingInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_FLOAT_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def keepIOStatusConfigInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_KEEP_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def pullDownInputInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_PULLL_DOWN_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def pullUpInputInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_PULL_UP_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def pushPullOutput(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_PUSH_PULL)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
	
	def wireOutputToOR(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_OR)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
		
	def wireOutputToAND(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_AND)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
		
	def wireOutputToORAndPullDown(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_OR_PULL_DOWN)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
		
	def wireOutputToANDPullUp(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_AND_PULL_UP)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
		
	def pushPullOutputInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_PUSH_PULL_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
	
	def wireOutputToORInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_OR_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
		
	def wireOutputToANDInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_AND_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
		
	def wireOutputToORAndPullDownInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_OR_PULL_DOWN_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)
		
	def wireOutputToANDPullUpInverted(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(IO_CONFIG_WIRED_AND_PULL_UP_INVERTED)
		self.sendCommand(CMD_IO_SetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_SetIOConfig)

	def getIOConfig(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		self.sendCommand(CMD_IO_GetIOConfig, tmp_data)
		return self.decodeResponse(CMD_IO_GetIOConfig)

	def setIOHigh(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(0x01)
		self.sendCommand(CMD_IO_SetIoValue, tmp_data)
		return self.decodeResponse(CMD_IO_SetIoValue)

	def setIOLow(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		tmp_data.append(0x00)
		self.sendCommand(CMD_IO_SetIoValue, tmp_data)
		return self.decodeResponse(CMD_IO_SetIoValue)
	
	def getIOValue(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		self.sendCommand(CMD_IO_GetIoValue, tmp_data)
		return self.decodeResponse(CMD_IO_GetIoValue)		

	def getADCValue(self, ioID):
		tmp_data = bytearray()
		tmp_data.append(ioID)
		self.sendCommand(CMD_IO_GetADCValue, tmp_data)
		return self.decodeResponse(CMD_IO_GetADCValue)		

	def getNumberOfSerialPorts(self):
		self.sendCommand(CMD_SER_GetNumberOfSerialPorts)
		return self.decodeResponse(CMD_SER_GetNumberOfSerialPorts)

	def configSerialPort(self, serialID, baudrate=BAUDRATE_115200, databits=0x08, parity=NO_PARITY, stopbits=0x01):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		#Update Baudrate
		tmp_data.append(baudrate)
		self.sendCommand(CMD_SER_SetBaudrate, tmp_data)
		self.decodeResponse(CMD_SER_SetBaudrate)
		#Update Databits
		tmp_data.pop()
		tmp_data.append(databits)
		self.sendCommand(CMD_SER_SetDatabits, tmp_data)
		self.decodeResponse(CMD_SER_SetDatabits)
		#Update Parity
		tmp_data.pop()
		tmp_data.append(parity)
		self.sendCommand(CMD_SER_SetParity, tmp_data)
		self.decodeResponse(CMD_SER_SetParity)
		#Update Stopbits
		tmp_data.pop()
		tmp_data.append(stopbits)
		self.sendCommand(CMD_SER_SetStopbits, tmp_data)
		self.decodeResponse(CMD_SER_SetStopbits)

	def getBaudrate(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_GetBaudrate, tmp_data)
		return self.decodeResponse(CMD_SER_GetBaudrate)

	def getDataBits(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand( CMD_SER_GetDatabits, tmp_data)
		return self.decodeResponse(CMD_SER_GetBaudrate)

	def getParity(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand( CMD_SER_GetParity, tmp_data)
		return self.decodeResponse(CMD_SER_GetParity)

	def getStopBits(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand( CMD_SER_GetStopbits, tmp_data)
		return self.decodeResponse(CMD_SER_GetStopbits)

	def transmitViaSerial(self, serialID, data):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		a = 0
		for c in data:
			tmp_data.append(c)
			a += 1
		dataSize[CMD_SER_Transmit] = a + 1
		self.sendCommand(CMD_SER_Transmit, tmp_data)
		return self.decodeResponse(CMD_SER_Transmit)

	def bytesWaitingToBeTransmitted(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_GetBytesInTxBuffer, tmp_data)
		return self.decodeResponse(CMD_SER_GetBytesInTxBuffer)

	def bytesReceived(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_GetBytesInRxBuffer, tmp_data)
		return self.decodeResponse(CMD_SER_GetBytesInRxBuffer)

	def readAndKeep(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_Receive, tmp_data)
		return self.decodeResponse(CMD_SER_Receive)

	def read(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_ReceiveAndClear, tmp_data)
		return self.decodeResponse(CMD_SER_ReceiveAndClear)

	def setDTRHigh(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		tmp_data.append(0x01)
		self.sendCommand(CMD_SER_SetDTR, tmp_data)
		return self.decodeResponse(CMD_SER_SetDTR)

	def setDTRLow(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		tmp_data.append(0x00)
		self.sendCommand(CMD_SER_SetDTR, tmp_data)
		return self.decodeResponse(CMD_SER_SetDTR)

	def getDTR(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_GetDTR, tmp_data)
		return self.decodeResponse(CMD_SER_GetDTR)
	
	def setRTSHigh(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		tmp_data.append(0x01)
		self.sendCommand(CMD_SER_SetRTS, tmp_data)
		return self.decodeResponse(CMD_SER_SetRTS)
	
	def setRTSLow(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		tmp_data.append(0x00)
		self.sendCommand(CMD_SER_SetRTS, tmp_data)
		return self.decodeResponse(CMD_SER_SetRTS)

	def getRTS(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_GetRTS, tmp_data)
		return self.decodeResponse(CMD_SER_GetRTS)

	def getDSR(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_GetDSR, tmp_data)
		return self.decodeResponse(CMD_SER_GetDSR)

	def getCTS(self, serialID):
		tmp_data = bytearray()
		tmp_data.append(serialID)
		self.sendCommand(CMD_SER_GetCTS, tmp_data)
		return self.decodeResponse(CMD_SER_GetCTS)

	def getNumberOfDevices(self):
		self.sendCommand(CMD_VND_GetNumberOfDevices)
		return self.decodeResponse(CMD_VND_GetNumberOfDevices)

	def GetDeviceInfo(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetDeviceInfo, tmp_data)
		return self.decodeResponse(CMD_VND_GetDeviceInfo)

	def setDeviceOn(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		tmp_data.append(0x01)
		self.sendCommand(CMD_VND_SetDeviceMode, tmp_data)
		return self.decodeResponse(CMD_VND_SetDeviceMode)

	def setDeviceOff(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		tmp_data.append(0x00)
		self.sendCommand(CMD_VND_SetDeviceMode, tmp_data)
		return self.decodeResponse(CMD_VND_SetDeviceMode)

	def getDeviceMode(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetDeviceMode, tmp_data)
		return self.decodeResponse(CMD_VND_GetDeviceMode)

	def getDeviceStatus(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetDeviceStatus, tmp_data)
		return self.decodeResponse(CMD_VND_GetDeviceStatus)

	def setDeviceCredit(self, deviceID, Credit):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		tmp_data.append(Credit)
		self.sendCommand(CMD_VND_SetDeviceMode, tmp_data)
		return self.decodeResponse(CMD_VND_SetDeviceMode)

	def getDeviceCredit(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetDeviceCredit, tmp_data)
		return self.decodeResponse(CMD_VND_GetDeviceCredit)

	def setInventory(self, deviceID,  inventory):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		tmp_data.append(inventory)
		self.sendCommand(CMD_VND_SetInventory, tmp_data)
		return self.decodeResponse(CMD_VND_SetInventory)

	def getInventory(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetInventory, tmp_data)
		return self.decodeResponse(CMD_VND_GetInventory)

	def SetInhibits(self, deviceID, inhibit):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		tmp_data.append((inhibit >> 8) & 0xFF)
		tmp_data.append(inhibit & 0xFF)
		self.sendCommand(CMD_VND_SetInventory, tmp_data)
		return self.decodeResponse(CMD_VND_SetInventory)

	def GetInhibit(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetInhibits, tmp_data)
		return self.decodeResponse(CMD_VND_GetInhibits)

	def setRouting(self, deviceID,  routing):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		tmp_data.append((routing >> 8) & 0xFF)
		tmp_data.append(routing & 0xFF)
		self.sendCommand(CMD_VND_SetRouting, tmp_data)
		return self.decodeResponse(CMD_VND_SetRouting)

	def GetRouting(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetRouting, tmp_data)
		return self.decodeResponse(CMD_VND_GetRouting)

	def PayoutByDenomination(self, payoutConfig):
		self.sendCommand(CMD_VND_PayoutByDenomination, payoutConfig)
		return self.decodeResponse(CMD_VND_PayoutByDenomination)

	def FloatByDenomination(self, payoutConfig):
		self.sendCommand(CMD_VND_FloatByDenomination, payoutConfig)
		return self.decodeResponse(CMD_VND_FloatByDenomination)

	def EmptyDevice(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_EmptyDevice, tmp_data)
		return self.decodeResponse(CMD_VND_EmptyDevice)

	def ClearDeviceError(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_ClearDeviceErrorStatus, tmp_data)
		return self.decodeResponse(CMD_VND_ClearDeviceErrorStatus)

	def GetLastPayout(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetLastPayout, tmp_data)
		return self.decodeResponse(CMD_VND_GetLastPayout)

	def GetTokenID(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_GetTokenID, tmp_data)
		return self.decodeResponse(CMD_VND_GetTokenID)

	def SaveInhibits(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_SaveInhibits, tmp_data)
		return self.decodeResponse(CMD_VND_SaveInhibits)

	def SaveRouting(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_SaveRoutings, tmp_data)
		return self.decodeResponse(CMD_VND_SaveRoutings)

	def ChangeDeviceCredits(self, changeConfig):
		self.sendCommand(CMD_VND_ChangeCredit, changeConfig)
		return self.decodeResponse(CMD_VND_ChangeCredit)

	def SetBezelColor(self, deviceID, red, green, blue):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		tmp_data.append(red)
		tmp_data.append(green)
		tmp_data.append(blue)
		self.sendCommand(CMD_VND_SetBezelColor, tmp_data)
		return self.decodeResponse(CMD_VND_SetBezelColor)

	def GetFloatPositions(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_NoteFloatGetPositions, tmp_data)
		return self.decodeResponse(CMD_VND_NoteFloatGetPositions)

	def DispenseLastNote(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_NoteFloatPayout, tmp_data)
		return self.decodeResponse(CMD_VND_NoteFloatPayout)

	def StackLastNote(self, deviceID):
		tmp_data = bytearray()
		tmp_data.append(deviceID)
		self.sendCommand(CMD_VND_NoteFloatToStacker, tmp_data)
		return self.decodeResponse(CMD_VND_NoteFloatToStacker)
