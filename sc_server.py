import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTED] {addr} disconnected.")
                break

            print(f"[{addr}] {msg}")
            sender_info = f"{addr[0]}:{addr[1]}"
            broadcast(msg, conn, sender_info)
        
    conn.close()
    clients.remove(conn)

def broadcast(message, sender_conn, sender_info):
    for client in clients:
        if client != sender_conn:
            client.send(message.encode(FORMAT))
            client.send(sender_info.encode(FORMAT))

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACITVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
