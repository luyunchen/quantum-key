from COWzip import *
from COWencryption import *
from Uploader import *
import os, shutil
from requests import get
import sys

def writeLocationData(port, name,ip):
    f = open(os.path.dirname(os.path.realpath(__file__))+"/ip.txt", "w")
    f.write(ip)
    f.close()
    p = open(os.path.dirname(os.path.realpath(__file__))+"/port.txt", "w")
    p.write(port)
    p.close()
    n = open(os.path.dirname(os.path.realpath(__file__))+"/name.txt", "w")
    n.write(name)
    n.close()


def createPrivate():
    print("Creating Dir")
    if (os.path.isdir(os.path.dirname(os.path.realpath(__file__))+"/VaultKey")):
        shutil.rmtree(os.path.dirname(os.path.realpath(__file__))+"/VaultKey")
        os.mkdir(os.path.dirname(os.path.realpath(__file__))+"/VaultKey")
    else:
        os.mkdir(os.path.dirname(os.path.realpath(__file__))+"/VaultKey")
    print("making key at" + str(os.path.dirname(os.path.realpath(__file__)))+"/VaultKey")
    createKey(os.path.dirname(os.path.realpath(__file__))+"/Vaultkey/")





def receiveVault():
    #   Can't decrypt an empty file!!!
    if (os.path.getsize("Vault.zip")>2000):
        decrypt("Vault.zip","VaultUnsafe.zip","TransportKey/")
        if (os.path.isdir("VaultKey")):
            decrypt("VaultUnsafe.zip","VaultNaked.zip","VaultKey/")
            unzip("VaultNaked.zip", "Vault")
        else:
            unzip("VaultUnsafe.zip", "Vault")
    else:
        os.system("md Vault")

def pushVault(ip,port):
    print("zipping")
    zip("Vault","VaultNaked")
    if (os.path.isdir("VaultKey")):
        encrypt("VaultNaked.zip","VaultUnsafe.zip","VaultKey/")
        encrypt("VaultUnsafe.zip","NewVault.zip","TransportKey/")
    else:
        encrypt("VaultNaked.zip","NewVault.zip","TransportKey/")
    
    print ("Sending...")
    uploadFile(ip,port,"NewVault.zip")
    uploadFile(ip,port,"name.txt")
    
    
    
#0=nothing
#1=delete
#2=shred
def purge(mode):
    if (mode=="Fast"):
        if (os.path.isdir("Vault")):
            shutil.rmtree("Vault")
        if (os.path.exists("VaultNaked.zip")):
            os.remove("VaultNaked.zip")
        if (os.path.exists("NewVault.zip")):
            os.remove("NewVault.zip")
        if (os.path.exists("Vault.zip")):
            os.remove("Vault.zip")
        if (os.path.exists("VaultUnsafe.zip")):
            os.remove("VaultUnsafe.zip")
        
    if (mode=="Secure"):
        try:
            if (os.path.isdir("Vault")):
                shutil.rmtree("Vault")
            if (os.path.exists("VaultNaked.zip")):
                os.rename('VaultNaked.zip','deletion')
            if (os.path.exists("deletion")):
                os.remove("deletion")
            if (os.path.exists("VaultUnsafe.zip")):
                os.rename('VaultUnsafe.zip','deletion')
            if (os.path.exists("deletion")):
                os.remove("deletion")

            if (os.path.exists("Vault.zip")):
                os.rename('Vault.zip','deletion')
            if (os.path.exists("deletion")):
                os.remove("deletion")
            if (os.path.exists("NewVault.zip")):
                os.rename('NewVault.zip','deletion')
            if (os.path.exists("deletion")):
                os.remove("deletion")
        except:
            print ("Stuff happened")