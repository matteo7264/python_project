# dns-server.py
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread, Lock
import sys


class DnsServer:
    def __init__(self, ip, port, csv_file="data.csv"):
        self.ip = ip
        self.port = port
        self.csv_file = csv_file

        self.lock = Lock()
        self.data = {}  # domain -> {"ip": "...", "code": "..."}

        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind((self.ip, self.port))
        print(f"serveur DNS en écoute sur {self.ip}:{self.port}")

        self.load_csv()

    def load_csv(self):
        # Lit le fichier UNE SEULE FOIS au démarrage et met tout en mémoire
        with open(self.csv_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue

                # Format: domain,ip,code
                parts = line.split(",")
                if len(parts) != 3:
                    continue  # ligne invalide, on ignore simplement

                domain = parts[0].strip()
                ip = parts[1].strip()
                code = parts[2].strip()

                self.data[domain] = {"ip": ip, "code": code}

    def handle_request(self, msg, client_addr):
        text = msg.decode(errors="replace").strip()

        # Requête simple: R=<DOMAINNAME>
        if text.startswith("R="):
            domain = text[2:].strip()

            with self.lock:
                if domain in self.data:
                    ip = self.data[domain]["ip"] # si le domaine existe dans les données en mémoire, je vais chercher l'ip liée à ce domaine
                    reply = f"R={domain},{ip}"
                else:
                    reply = f"R={domain},NXDOMAIN"

            self.server_socket.sendto(reply.encode(), client_addr)
            return

        # Requête update: U=<DOMAINNAME>,IP=<IP>,CODE=<CODE>
        if text.startswith("U="):
            # Exemple: U=example.com,IP=192.168.1.2,CODE=mysecretcode
            parts = text.split(",")
            if len(parts) != 3:
                self.server_socket.sendto(f"U=,UNAUTHORIZED".encode(), client_addr)
                return

            domain = parts[0].replace("U=", "").strip()
            new_ip = parts[1].replace("IP=", "").strip()
            given_code = parts[2].replace("CODE=", "").strip()

            with self.lock:
                if domain in self.data and self.data[domain]["code"] == given_code:
                    self.data[domain]["ip"] = new_ip
                    reply = f"U={domain},IP={new_ip},OK"
                else:
                    reply = f"U={domain},IP={new_ip},UNAUTHORIZED"

            self.server_socket.sendto(reply.encode(), client_addr)
            return

        self.server_socket.sendto("ERROR".encode(), client_addr)

    def listen_loop(self):
        while True:
            msg, client_addr = self.server_socket.recvfrom(2048)
            Thread(target=self.handle_request, args=[msg, client_addr]).start()


if len(sys.argv) != 3:
    print("syntaxe : python dns-server.py <IP> <PORT>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

server = DnsServer(HOST, PORT, "data.csv")
server.listen_loop()