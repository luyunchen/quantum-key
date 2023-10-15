import requests
import tkinter
import tkinter.messagebox
import customtkinter
import ctypes
from ClientMain import *


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ServerMenu(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        deviceList = ["None", "Fast", "Secure"]
        with open('port.txt') as f:
            first_line = f.readline()
        serverPort = first_line
        with open('ip.txt') as i:
            first_line = i.readline()
        serverIP = first_line
        #window config
        self.geometry("800x500")
        self.title("Quantum Key - Configuration")
        self.resizable(0,0)

        #frames
        self.titleFrame = customtkinter.CTkFrame(self, width=600, height=100)
        self.titleFrame.place(relx=0.5, rely=.15, anchor=tkinter.CENTER)
        self.settingsFrame = customtkinter.CTkFrame(self, width=300, height=300)
        self.settingsFrame.place(relx=.7, rely=0.6, anchor=tkinter.CENTER)
        self.fileFrame = customtkinter.CTkFrame(self, width=300, height=300)
        self.fileFrame.place(relx=.3, rely=0.6, anchor=tkinter.CENTER)

        #titles
        self.mainTitle = customtkinter.CTkLabel(self.titleFrame, text="QUANTUM KEY", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.mainTitle.place(relx=.5, rely=.3, anchor=tkinter.CENTER)
        self.secondaryTitle = customtkinter.CTkLabel(self.titleFrame, text="Safe File Transfer Protocol", font=customtkinter.CTkFont(size=20))
        self.secondaryTitle.place(relx=.5, rely=.7, anchor=tkinter.CENTER)

        #button
        self.downloadFiles = customtkinter.CTkButton(self.settingsFrame, width=275, height=50, text="PULL WORKSPACE", font=customtkinter.CTkFont(size=12, weight="bold"), command=self.download_files_event)
        self.downloadFiles.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        self.disconnect = customtkinter.CTkButton(self.settingsFrame, width=275, height=50, text="CLOSE WORKSPACE", font=customtkinter.CTkFont(size=12, weight="bold"), command=self.disconnect_event, fg_color="#EB2222", hover_color="#991616")
        self.disconnect.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
        self.sync = customtkinter.CTkButton(self.fileFrame, width=275, height=50, text="PUSH WORKSPACE", font=customtkinter.CTkFont(size=12, weight="bold"), command=self.sync_event)
        self.sync.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        #dropdown
        self.selectDevice = customtkinter.CTkOptionMenu(self.settingsFrame, values=deviceList)
        self.selectDevice.place(relx=.1, rely=.2, anchor=tkinter.W)
        self.selectDeviceText = customtkinter.CTkLabel(self.settingsFrame, text="Close mode:")
        self.selectDeviceText.place(relx=.1, rely=.1, anchor=tkinter.W)
        self.selectClientText = customtkinter.CTkLabel(self.fileFrame, text="Connected to " + serverIP + ":"+ serverPort)
        self.selectClientText.place(relx=.5, rely=.1, anchor=tkinter.N)

        #serverinfo
        self.serverIP = customtkinter.CTkEntry(self.settingsFrame, placeholder_text="Server IP")
        self.serverIP.place(relx=.1, rely=.4, anchor=tkinter.W)
        self.serverIP.insert(0,serverIP)
        self.serverIP.configure(state="disabled")
        self.serverPort = customtkinter.CTkEntry(self.settingsFrame, placeholder_text="Server Port")
        self.serverPort.place(relx=.1, rely=.5, anchor=tkinter.W)
        self.serverPort.insert(0,serverPort)
        self.serverPort.configure(state="disabled")


    def download_files_event(self):
        if (not os.path.isdir("Vault")):
            os.mkdir("Vault")

        print ("Cleaning...")
        shutil.rmtree("Vault")
        
        with open('port.txt') as f:
            first_line = f.readline()
        serverPort = first_line
        with open('ip.txt') as i:
            first_line = i.readline()
        serverIP = first_line
        with open('name.txt') as i:
            first_line = i.readline()
        url = "http://"+serverIP + ":"+ serverPort+"/Vault_"+first_line+".zip"
        print("Pulling: " + url)
        open('Vault.zip', 'wb').write(requests.get(url, allow_redirects=True).content)
        print("Decrypting")
        receiveVault()
        print("Opening...")
        os.system("start Vault")

    def disconnect_event(self):
        disconnectWarning = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to shut down the server? Your files will be decrypted, and the clients won't be able to access your files anymore.", "Disconnect", 4)
        #6 = yes, 7 = no
        print (disconnectWarning)
        print (self.selectDevice.get())
        if (disconnectWarning==6):
            purge(self.selectDevice.get())
            exit()

    def sync_event(self):
        print("Syncing...")
        with open('port.txt') as f:
            first_line = f.readline()
        serverPort = first_line
        with open('ip.txt') as i:
            first_line = i.readline()
        serverIP = first_line
        pushVault(serverIP,serverPort)
        


serverMenu = ServerMenu()
serverMenu.iconbitmap("QuantumKey.ico")
serverMenu.mainloop()