import socket
import threading

HOST = '127.0.0.1'
PORT = 9898

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients = []
nicknames = []

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def broadcast(message):
    for client in clients:
        client.send(message)

def receive():
    while True:
        client , address = server.accept()
        print(f"Conected with {str(address)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}")
        broadcast(f"{nickname} joined chat\n".encode('utf-8'))
        client.send("Conneted to server\n".encode('utf-8'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server Running")
receive()







