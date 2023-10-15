from ServerMain import *
import os

while (True):
    if (not os.path.exists("workspace/name.txt")):
        #Constantly parses TransportKey
        subdirs = [ f.path for f in os.scandir("TransportKey") if f.is_dir() ]
        for folders in subdirs:
            folder = os.path.basename(folders)
            
            if (not os.path.exists("Workspace/Vault_"+folder+".zip")):
                if (os.path.isdir("TransportKey/" + folder)):
                    if (os.path.exists("TransportKey/" + folder+"/private.pem")):
                        if (os.path.exists("TransportKey/" + folder+"/public.pem")):
                            print (folder + " Has been removed! Recreating...")
                            pushVault(folder)       
    else:
        print("Incoming!")
        
        with open('workspace/name.txt') as f:
            first_line = f.readline()
        name = first_line
        print(name)
        receiveVault(name)
        for filename in os.listdir("workspace"):
            f = os.path.join("Workspace", filename)
            os.remove(f)
        print("Done!!")