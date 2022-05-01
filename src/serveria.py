#!/usr/bin/python3

import json
import socket 
from threading import Thread 
from socketserver import ThreadingMixIn
import recomana_jobs

# global conn

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    CONN_DELIMITER = ' '
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print(f"[+] New server socket thread started for {ip}: {port}")
 
    def run(self):
        query = self.parse_query(conn)
        print("Server received data:", query)
        cmd = query.get('cmd')
        res = {"error": f"Watafak do you expect me to do? I don't understand your {cmd}"}

        if cmd == "OFF":
            skills = query.get('skills')
            if skills is None:
                res = {"error": "Skills is fucking None"}
            else:
                res = recomana_jobs.recomend_job_by_keywords([s.upper() for s in skills])
                res['offers'] = [i + 1 for i in res['offers']]

        if cmd == "SSK":
            skills = query.get('skills')
            if skills is None:
                res = {"error": "Skills is fucking None"}
            else:
                res = recomana_jobs.predict_knc([s.upper() for s in skills])

        self.send_reply(conn, res)

    def parse_query(self, conn):
        # length = ""
        # last = conn.recv(1).decode("utf-8")
        # while last != self.CONN_DELIMITER:
        #     length += last
        #     last = conn.recv(1).decode("utf-8")
        # rawjson = conn.recv(int(length))
        # return json.loads(rawjson)
        length  = conn.recv(6).decode("utf-8")
        # conn.recv(1) # Ignore separator
        rawjson = conn.recv(int(length))
        print("Server received data of length:", length, " → ", rawjson)
        return json.loads(rawjson)

    def send_reply(self, conn, data):
        rawjson = json.dumps(data).encode('utf-8')
        size    = len(rawjson)
        print(f"Replying with {size:0>6} bytes → {rawjson}")
        conn.send((f"{size:0>6}").encode('utf-8') + rawjson)
        return True

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP   = '0.0.0.0'
TCP_PORT = 8383
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# tcpServer.settimeout(20) # Mala idea aquí
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True: 
    tcpServer.listen(4)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    conn, (ip, port) = tcpServer.accept()
    print(f"Connection from {ip}:{port}")
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)
 
for t in threads: 
    t.join() 
