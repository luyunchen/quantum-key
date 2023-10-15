import pickle
import tkinter
import time
import wmi
import random
import tkinter.messagebox
import customtkinter
import socket
import os
import win32api
from requests import get

from ServerMain import *


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ServerWelcome(customtkinter.CTk):
	def __init__(self):
		super().__init__()
		
		deviceList = (win32api.GetLogicalDriveStrings().split('\000')[:-1])
		ip = get('https://api.ipify.org').content.decode('utf8')
		serverIP = ip
		serverPort = "1984"
		#window config
		self.geometry("800x500")
		self.title("Quantum USB - Configuration")
		self.resizable(0,0)

		#frames
		self.titleFrame = customtkinter.CTkFrame(self, width=600, height=100)
		self.titleFrame.place(relx=0.5, rely=.15, anchor=tkinter.CENTER)
		self.settingsFrame = customtkinter.CTkFrame(self, width=300, height=300)
		self.settingsFrame.place(relx=.7, rely=0.6, anchor=tkinter.CENTER)

		#titles
		self.mainTitle = customtkinter.CTkLabel(self.titleFrame, text="Quantum USB", font=customtkinter.CTkFont(size=30, weight="bold"))
		self.mainTitle.place(relx=.5, rely=.3, anchor=tkinter.CENTER)
		self.secondaryTitle = customtkinter.CTkLabel(self.titleFrame, text="Safe File Transfer Protocol", font=customtkinter.CTkFont(size=20))
		self.secondaryTitle.place(relx=.5, rely=.7, anchor=tkinter.CENTER)

		#button
		self.createServer = customtkinter.CTkButton(self, width=300, height=150, text="CREATE SERVER", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.create_server_event)
		self.createServer.place(relx=0.3, rely=0.45, anchor=tkinter.CENTER)
		self.importFiles = customtkinter.CTkButton(self.settingsFrame, width=275, height=50, text="Refresh devices/IP", font=customtkinter.CTkFont(size=12, weight="bold"), command=self.import_files_event)
		self.importFiles.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

		#dropdown
		self.selectDevice = customtkinter.CTkOptionMenu(self.settingsFrame, values=deviceList)
		self.selectDevice.place(relx=.1, rely=.2, anchor=tkinter.W)
		self.selectDeviceText = customtkinter.CTkLabel(self.settingsFrame, text="Please select a physical device.*")
		self.selectDeviceText.place(relx=.1, rely=.1, anchor=tkinter.W)

		#serverinfo
		self.serverIP = customtkinter.CTkEntry(self.settingsFrame, placeholder_text="Server IP")
		self.serverIP.place(relx=.1, rely=.4, anchor=tkinter.W)
		self.serverIP.insert(0,serverIP)
		self.serverPort = customtkinter.CTkEntry(self.settingsFrame, placeholder_text="Server Port")
		self.serverPort.place(relx=.1, rely=.5, anchor=tkinter.W)
		self.serverPort.insert(0,serverPort)

		#vaultencryption
		self.vaultEncryption = customtkinter.CTkCheckBox(self.settingsFrame, text="Vault Encryption**")
		self.vaultEncryption.place(relx=.1, rely=.7, anchor=tkinter.W)

		#infotext
		self.infoMedium = customtkinter.CTkTextbox(self, width=300, height=125, wrap="word")
		self.infoMedium.place(relx=0.3, rely=0.75, anchor=tkinter.CENTER)
		self.infoMedium.insert(0.0, "*A physical device is used to store encryption keys, avoiding the need for on-the-fly key exchanges.\n" + "**Vault Encryption is optional extra security mesure used if the server is distrusted. With this mode, data recovery becomes impossible if keys are inaccessible.")
		self.infoMedium.configure(state="disabled")

	def import_files_event(self):
		os.system("start QUANTUMKEY_Server_Launcher.bat")
		exit()

	def create_server_event(self):
		firstTime(wmi.WMI().Win32_LogicalDisk()[(win32api.GetLogicalDriveStrings().split('\000')[:-1]).index(self.selectDevice.get())].VolumeName,self.selectDevice.get(),self.vaultEncryption.get(),self.serverPort.get(),self.serverIP.get())
		f = open("port.txt", "w")
		f.write(self.serverPort.get())
		f.close()
		os.system("start QUANTUMKEY_Server_Launcher.bat")
		exit()



serverWelcome = ServerWelcome()
serverWelcome.mainloop()