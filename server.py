from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from signal import signal, SIGINT
import sys
import os

WELCOME_MSG = 'Welcome to our chat. Enter your name.'

def incomming_connections():

    while True:

        client, addr = SERVER.accept()
        print(f'A client has connected {addr}')
        client.send(WELCOME_MSG.encode())
        Thread(target=single_client, args=(client,)).start()

def single_client(client):

    client_name = client.recv(BUFFERSIZE).decode()
    welcome_msg = f'Welcome {client_name}. If you want to exit type exit() or press Ctrl+D.'
    client.send(welcome_msg.encode())
    chat_msg = f'{client_name} has joined the room'
    broadcast_msg(chat_msg.encode())
    clients[client] = client_name

    while True:
        msg = client.recv(BUFFERSIZE)

        if msg == 'online()'.encode('utf8'):
            num_clients = get_clients()
            print(num_clients)
        elif msg == EXIT_STR.encode('utf8'):
            print(f'{clients[client]} has disconnected ')
            client.send('You are leaving the room...'.encode())
            client.close()
            del clients[client]
            broadcast_msg(f'{client_name} has left the room'.encode())
            break
        else:
            broadcast_msg(msg, client_name + ': ')

def get_clients():
    return len(clients)

def broadcast_msg(msg, name=""):

    for client in clients:
        client.send(name.encode() + msg)
        
if __name__ == "__main__":

    clients = {}

    HOST = '127.0.0.1'
    PORT = 33336
    BUFFERSIZE = 1024
    ADDR = (HOST, PORT)
    EXIT_STR = "exit()"
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(2)

    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=incomming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()