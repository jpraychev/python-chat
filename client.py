from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from signal import signal, SIGINT
import sys
import os 

def receive_msg():
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            print(msg)
        except OSError as error:
            return error

def send_msg():
    while True:
        try:
            msg = input()
            if msg != 'exit()':
                client_socket.send(msg.encode('utf8'))
            else:
                clean_exit()
        except EOFError:
            clean_exit()

def clean_exit():
    client_socket.send('exit()'.encode('utf8'))
    client_socket.close()
    sys.exit(0)

def handler(signal_received, frame):
    clean_exit()

if __name__ == '__main__':
    
    signal(SIGINT, handler)
    
    HOST = '127.0.0.1'
    PORT = 33336

    BUFFERSIZE = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive_msg)
    receive_thread.start()
    
    send_msg()






    