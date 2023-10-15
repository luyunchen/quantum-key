from COWzip import *
from COWencryption import *
import os, shutil
import subprocess


def createPublic(keyName, usbPort):

    print ("creating directory: " + "TransportKey/"+keyName)
    try:  
        os.mkdir("TransportKey/"+keyName)  
    except OSError as error:  
        print("Already exists!")   

    print ("deleting potential previous key")
    #clears prev public key
    shutil.rmtree("TransportKey/"+keyName)
    
    print ("creating new dirs for server keys")
    os.mkdir("TransportKey/"+keyName)
    print("creating key")
    createKey("TransportKey/"+keyName+"/")

    #copys it to the key
    print("copying keys to usb")
    print("at::: " +usbPort+"/QuantumKey/TransportKey_")
    shutil.copy(src="TransportKey/"+keyName+"/private.pem", dst=usbPort+"QuantumKey/TransportKey/private.pem")  
    shutil.copy(src="TransportKey/"+keyName+"/public.pem", dst=usbPort+"QuantumKey/TransportKey/public.pem")  

    

def firstTime(keyName, usbPort, privateKey, socket,ip):
    
    print ("cleaning usb...")
    try:
        shutil.rmtree(usbPort+"QuantumKey")
    except OSError as error:
        print ("fresh key!")
    
    print("Creating directories on USB")
    os.mkdir(usbPort+"QuantumKey")
    os.mkdir(usbPort+"QuantumKey/TransportKey")
    
    print("Starting public key...")
    createPublic(keyName, usbPort)
    print ("copying client code")
    
    for root, dirs, files in os.walk("Client"):
        for file in files:
            mysrc_file = os.path.join(root, file)
            shutil.copy2(mysrc_file, usbPort+"QuantumKey")
            
    
    
    print("Writing socked data")
    os.system("python "+usbPort+"QuantumKey/CreateSocketData.py " + socket+ " "+keyName + " " + ip)
    
    
    print ("First client created!")
    
    if (privateKey==1):
        print("Creating private key...")
        print("Asking client...")
        os.system("python "+usbPort+"QuantumKey/CreatePrivate.py")

    



def pushVault(keyName):
    if (os.path.exists("Vault/PRIVATE_Vault.zip")):
        shutil.copyfile("Vault/PRIVATE_Vault.zip","VaultUnsafe.zip")
    else:
        zip("Vault", "VaultUnsafe")
    encrypt("VaultUnsafe.zip","Vault.zip","TransportKey/"+keyName+"/")
    os.remove("VaultUnsafe.zip")
        
    shutil.copyfile("Vault.zip", "Workspace/Vault_"+keyName+".zip")
    
    os.remove("Vault.zip")
    
    

def receiveVault(keyName):
    decrypt("workspace/NewVault.zip","VaultUnsafe.zip","TransportKey/"+keyName+"/")
    try:    
        unzip("VaultUnsafe.zip", "Vault")
    except:
        shutil.copyfile("VaultUnsafe.zip","Vault/PRIVATE_Vault.zip")
    os.remove("VaultUnsafe.zip")