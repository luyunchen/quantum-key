import tkinter
import tkinter.messagebox
import customtkinter
import ctypes
import os
import wmi
import win32api
from requests import get
from ServerMain import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SelectDeviceWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        deviceList = (win32api.GetLogicalDriveStrings().split('\000')[:-1])
        
        self.selectNewKeyText = customtkinter.CTkLabel(self, text="Select your new key.")
        self.selectNewKeyText.place(relx=.5,rely=.2, anchor=tkinter.CENTER)
        self.selectNewKey = customtkinter.CTkOptionMenu(self, values=deviceList)
        self.selectNewKey.place(relx=.5,rely=.4, anchor=tkinter.CENTER)
        self.done = customtkinter.CTkButton(self, width=100, height=50, text="Done", command=self.done_event)
        self.done.place(relx=0.3, rely=0.7, anchor=tkinter.N)
        self.cancel = customtkinter.CTkButton(self, width=100, height=50, text="Cancel", command=self.cancel_event)
        self.cancel.place(relx=0.7, rely=0.7, anchor=tkinter.N)
    def done_event(self):
        with open('tmpDevice.txt') as f:
            device1 = f.readline()
        print("Copy:   " + device1 + " to " + self.selectNewKey.get())
        shutil.copytree(device1+"QuantumKey",  self.selectNewKey.get()+"QuantumKey")
        name=wmi.WMI().Win32_LogicalDisk()[(win32api.GetLogicalDriveStrings().split('\000')[:-1]).index(self.selectNewKey.get())].VolumeName

        with open(self.selectNewKey.get()+"QuantumKey/name.txt", 'w') as the_file:
            the_file.write(name)

        createPublic(name,self.selectNewKey.get())
        
        
        self.destroy()
    def cancel_event(self):
        self.destroy()


class ServerMenu(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.selectdevice_window = None
        deviceList = (win32api.GetLogicalDriveStrings().split('\000')[:-1])
        subdirs = [ f.path for f in os.scandir("TransportKey") if f.is_dir() ]
        clientList = []
        for folders in subdirs:
            clientList.append(os.path.basename(folders))
        

        ip = get('https://api.ipify.org').content.decode('utf8')
        serverIP = ip
        with open('port.txt') as f:
            first_line = f.readline()
        serverPort = first_line
        serverStatus = "online"
        #window config
        self.geometry("800x500")
        self.title("Quantum Key - Configuration")
        self.resizable(0,0)

        #frames
        self.titleFrame = customtkinter.CTkFrame(self, width=600, height=100)
        self.titleFrame.place(relx=0.5, rely=.15, anchor=tkinter.CENTER)
        self.settingsFrame = customtkinter.CTkFrame(self, width=300, height=275)
        self.settingsFrame.place(relx=.7, rely=0.65, anchor=tkinter.CENTER)
        self.authFrame = customtkinter.CTkFrame(self, width=300, height=275)
        self.authFrame.place(relx=.3, rely=0.65, anchor=tkinter.CENTER)

        #titles
        self.mainTitle = customtkinter.CTkLabel(self.titleFrame, text="QUANTUM KEY", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.mainTitle.place(relx=.5, rely=.3, anchor=tkinter.CENTER)
        self.secondaryTitle = customtkinter.CTkLabel(self.titleFrame, text="Safe File Transfer Protocol", font=customtkinter.CTkFont(size=20))
        self.secondaryTitle.place(relx=.5, rely=.7, anchor=tkinter.CENTER)

        self.clientManagement = customtkinter.CTkLabel(self.settingsFrame, text="Client Management", font=customtkinter.CTkFont(size=20))
        self.clientManagement.place(relx=.5, rely=.1, anchor=tkinter.CENTER)
        self.serverManagement = customtkinter.CTkLabel(self.authFrame, text="Server Management", font=customtkinter.CTkFont(size=20))
        self.serverManagement.place(relx=.5, rely=.1, anchor=tkinter.CENTER)

        #button
        self.newUSB = customtkinter.CTkButton(self.settingsFrame, width=275, height=50, text="ADD NEW KEY TO NETWORK", font=customtkinter.CTkFont(size=12, weight="bold"), command=self.newUSB_event)
        self.newUSB.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.disconnect = customtkinter.CTkButton(self.authFrame, width=275, height=50, text="DISCONNECT", font=customtkinter.CTkFont(size=12, weight="bold"), command=self.disconnect_event, fg_color="#EB2222", hover_color="#991616")
        self.disconnect.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        #self.delete = customtkinter.CTkButton(self.authFrame, width=100, height=50, text="DELETE CLIENT", command=self.delete_client_event, fg_color="#EB2222", hover_color="#991616")
        #self.delete.place(relx=0.7, rely=0.5, anchor=tkinter.N)
        #self.reroll = customtkinter.CTkButton(self.authFrame, width=100, height=50, text="REROLL KEY", command=self.reroll_event)
        #self.reroll.place(relx=0.3, rely=0.5, anchor=tkinter.N)

        self.delete = customtkinter.CTkButton(self.authFrame, width=275, height=50, text="DELETE CLIENT", font=customtkinter.CTkFont(size=12), command=self.delete_client_event, fg_color="#EB2222", hover_color="#991616")
        self.delete.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.reroll = customtkinter.CTkButton(self.settingsFrame, width=275, height=50, text="REROLL KEY", font=customtkinter.CTkFont(size=12), command=self.reroll_event)
        self.reroll.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        #dropdown
        self.selectDevice = customtkinter.CTkOptionMenu(self, values=deviceList, width = 250)
        self.selectDevice.place(relx=.68, rely=.28, anchor=tkinter.N)
        self.selectClient = customtkinter.CTkOptionMenu(self, values=clientList, width=250)
        self.selectClient.place(relx=.32, rely=.28, anchor=tkinter.N)


        #status
        self.status = customtkinter.CTkLabel(self, text="Status: " + serverStatus + " (" + serverIP + ":" + serverPort + ")")
        self.status.place(relx=.25, rely=.95, anchor=tkinter.CENTER)

    def disconnect_event(self):
        disconnectWarning = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to shut down the server?", "Disconnect", 4)
        if (disconnectWarning==6):
            os.system("taskkill /f /im python*")
        #6 = yes, 7 = no

    def reroll_event(self):
        createPublic(self.selectClient.get(),self.selectDevice.get())
    
    def delete_client_event(self):
        deleteWarning = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to delete this client?", "Delete client", 4)
        print(deleteWarning)
        #6 = yes, 7 = no
        if (deleteWarning==6):
            shutil.rmtree("TransportKey/"+self.selectClient.get())
            os.remove("Workspace/Vault_" + self.selectClient.get()+".zip")

    def newUSB_event(self):
        with open('tmpDevice.txt', 'w') as the_file:
            the_file.write(self.selectDevice.get())
        if self.selectdevice_window is None or not self.selectdevice_window.winfo_exists():
            self.selectdevice_window = SelectDeviceWindow(self)
            self.selectdevice_window.focus()
        else:
            self.selectdevice_window.focus()



serverMenu = ServerMenu()
serverMenu.iconbitmap("QuantumKey.ico")
serverMenu.mainloop()