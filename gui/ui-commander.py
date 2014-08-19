from tkinter import *
from tkinter import ttk

import time

port="/dev/ttyUSB0"

def connectToUI():
	print("connecting to "+port)
	return

def resetDevice():
	print("Resettign device")
	return

def updatePanel():
	print("Checking if a new version exists ..")
	time.sleep(1)
	print("This tool is already up to date !")
	return

def exitProgram():
	print("Quitting program")
	quit()
	return
def activateLog():
	print("Activating Log")
	return
	
def saveLog():
	print("Saving log to file ..")
	return

def showAbout():
	print("About")
	return

#Create Main Window
root = Tk()

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.title("Universal Interface Commander")

#Create top menu
root.option_add('*tearOff', FALSE)

menubar = Menu(root)
root['menu'] = menubar

menu_file = Menu(menubar)
menu_utilities = Menu(menubar)
menu_help = Menu(menubar)

menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_utilities, label='Utilities')
menubar.add_cascade(menu=menu_help, label='Help')

menu_file.add_command(label='Connect', command=connectToUI)
menu_file.add_separator()
menu_file.add_command(label='Reset Device', command=resetDevice)
menu_file.add_separator()
menu_file.add_command(label='Update Current Panel', command=updatePanel)
menu_file.add_separator()
menu_file.add_command(label='Exit', command=exitProgram)

menu_utilities.add_command(label='Log commands', command=activateLog)
menu_utilities.add_separator()
menu_utilities.add_command(label='Save log', command=saveLog)

menu_help.add_command(label='About', command=showAbout)

#Start the program
root.mainloop()
