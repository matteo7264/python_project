import random
import string
from threading import Thread, Lock
from socket import socket, AF_INET, SOCK_DGRAM

def parse_data():
    with open("data.csv") as f:
        for line in f.readlines():
            domain, ip, code = line.split(',')
            code = code.strip()
            records[domain] = {"ip": ip, "code": code}

def random_ip():
    return '.'.join((
            str(random.randint(0,255)),
            str(random.randint(0, 255)),
            str(random.randint(0, 255)),
            str(random.randint(0, 255))
    ))

def client():
    with socket(AF_INET, SOCK_DGRAM) as sock:

        domain = random.choice(list(records.keys()))
        ip = random_ip()

        if random.randint(0,1):

            if random.randint(0, 1):
                domain = ''.join((random.choices(string.ascii_letters, k=10))) + ".com"

            request = "R=" + domain

        else:

            if random.randint(0,1):
                code = records[domain]["code"]
            else:
                code = ''.join((random.choices(string.ascii_letters, k=20)))

            request = "U=" + domain + ",IP=" + ip + ",CODE=" + code

        sock.sendto(request.encode(), ("127.0.0.1", 7000))
        response, _ = sock.recvfrom(1024)

        lock.acquire()
        print("REQUEST:", request, "\n   RESPONSE:", response.decode())
        lock.release()

records = dict()
parse_data()
lock = Lock()

for i in range(200):
    Thread(target=client, args=[]).start()
