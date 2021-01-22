#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8888
BUFFER_SIZE = 1024

def handle_request(conn,addr,g_s):
    full_data = conn.recv(BUFFER_SIZE)
    g_s.sendall(full_data)
    g_s.shutdown(socket.SHUT_WR)

    back_data = g_s.recv(BUFFER_SIZE)
    conn.send(back_data)


    
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as g_s:
                #recieve data, wait a bit, then send it back
                #full_data = conn.recv(BUFFER_SIZE)
                #time.sleep(0.5)
                g_s.connect((socket.gethostbyname('www.google.com'), 80))

                p = Process(target=handle_request, args=(conn,addr, g_s))
                p.daemon = True
                p.start()

                #g_s.sendall(full_data)
                #print('DATA FROM CLIENT TO SEREVER', full_data)
                #g_s.shutdown(socket.SHUT_WR)
                #back_data = g_s.recv(BUFFER_SIZE)
                #conn.sendall(back_data)
                #print('DATA FROM GOOGLE TO SERVER', back_data)
            
            conn.close()

if __name__ == "__main__":
    main()
