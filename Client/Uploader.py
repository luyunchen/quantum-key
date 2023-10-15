import requests
import os
import socket
import time


def uploadFile(IPAddr, port,fileName):
    

    url = 'http://' +str(IPAddr) +':' +str(port)  +'/'+fileName
    print(url)

    file_path = fileName  # Replace with the path to the file you want to upload

    with open(file_path, 'rb') as file:
        response = requests.put(url, data=file)

    if response.status_code == 200:
        print('File uploaded successfully')
    else:
        print(f'Did thing: {response.status_code} - {response.text}')