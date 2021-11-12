import socket
import select #hanles the

# constants
HEADER_LENGTHS = 10
IP = "127.0.0.1"
PORT = 3000

#building the server
server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)#AF~ Address Family
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
server_socket.bind((IP , PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

#function for recieving the messages from the client
def rec_msg(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTHS)
        if not len(message_header):
            return False
        message_len = int(message_header.decode('utf-8').strip())
        return {"header":message_header,"data":client_socket.recv(message_len)}
    except:
        return False

while True:
    read_sockets , _ , exception_sockets = select.select(sockets_list,[],sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket , client_address = server_socket.accept()

            user = rec_msg(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print("*******************************")
            print(f"New Connection was accepted from {client_address[0]}:{client_address[1]} username is : {user['data'].decode('utf-8')}")
            print("*******************************")
        else:
            message = rec_msg(notified_socket)
            if message is False:
                print(f"We Lost the Connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
            