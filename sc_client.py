import socket
import threading
import sys

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "IPV4-HERE"  # Server's computer ipv4 address
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def send_msg():
    while True:
        sen_msg = input('\nMessage: ')
        if sen_msg == '!DISCONNECT':
            send(DISCONNECT_MESSAGE)
            print('Disconnected from the server.')
            break
        send(sen_msg)

def receive_msg():
    while True:
        message_length = client.recv(HEADER).decode(FORMAT)
        message_info = client.recv(HEADER).decode(FORMAT)
        sys.stdout.write('\r' + ' ' * 10 + '\r')
        sys.stdout.flush()
        print(f"[('{message_info.split(':')[0]}', {message_info.split(':')[1]})] {message_length}")
        print("Message: ", end="", flush=True)

# Start a separate thread for receiving messages
receive_thread = threading.Thread(target=receive_msg)
receive_thread.start()

# Start a separate thread for sending messages
send_thread = threading.Thread(target=send_msg)
send_thread.start()
