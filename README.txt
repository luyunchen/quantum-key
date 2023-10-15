Thanks for using QuantumKey!

QuantumKey is a quantum-safe self hosted file syncing network.

With QuantumKey, you can create a safe workspace with as many clients as you want! The principle is to use physical keys to store keys to decrypt the workspace that's shared by the server.

The code is made with python, so you need to install Python 3 beforehand (if you're on Windows, use Microsoft Store).

To start, you need to configure your server. Run QUANTUMKEY_Server_Launcher.bat. It will install all the python libraries. Afterwards, a window will pop up. Insert a physical device (USB key, SD card, etc.) and refresh the device list if needed in order to select it. You need to set your server IP. The one that's there is your public IP. If you want to share your workspace around the world, you'll need to open a port on your router and set that port. If you want to share your workspace on a local network, you'll need to modify the IP to your local IP (you can fetch using cmd). Activate the vault encryption to encrypt the files on the server and provide an extra layer of protection for your workspace. Then, create the server.
The menu will open and you'll be able to see the authenticated keys. It'll take the USB key name. If you want to make another key, you need to select the device that has the authenticated key and select "Add a new key". Select another physical device, and press "done". Now, you should have another key ready. If you want to see it, you'll need to disconnect the server and start the launcher again. Now, you should be able to see it.

The client program will already be installed on the physical devices. Once the server is online, you can plug a physical device that's authenticated with the server and choose to "Pull workspace". If the port is opened and everything is set up correctly, you should be able to see a new window containing an empty workspace. You can add files, and once you're done, you can send it back using "Push workspace". Choose your close mode and "Disconnect":
"None" will keep the workspace on your computer;
"Fast" will delete the workspace;
"Secure" will shred the workspace.
You can try doing the same thing with another authenticated key or with another computer and you should be able to see the workspace!