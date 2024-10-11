import socket
import threading
import random
import string
import sys
from dataHandle import *

# Store user_id and socket
clients_list = {}

def generate_unique_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def link_handler(link, client):
    user_id = generate_unique_id()
    clients_list[user_id] = link
    link.sendall(f'Welcome! Your ID is: {user_id}'.encode())
    print(f'{user_id} connected')
    # print('server start to receiving msg from [%s:%s]....' % (client[0], client[1]))
    while True:
        try:
            client_data = link.recv(1024).decode()
            if not client_data:
                print(f'{user_id} disconnected')
                break
            
            # Show exisiting users
            if client_data =="ls":
                keys = clients_list.keys()
                client_list = ', '.join(keys)
                client_list = 'User list: '+ client_list
                link.sendall(client_list.encode())
            
            if ":" in client_data:
                recipient, msg = client_data.split(':', 1)
                # Forward msg to specified user
                if recipient in clients_list:
                    recipient_socket = clients_list[recipient]
                    forward_message = f"{user_id} said: {msg}"
                    store_chat_history(user_id,recipient,msg)
                    recipient_socket.sendall(forward_message.encode())
                # Get chat history with specified user
                elif recipient == 'hs':
                    link.sendall(retrieve_chat_history(user_id,msg).encode())
                else:
                    link.sendall(f"{recipient} is not connected.".encode())

            if client_data == "exit":
                print('Communication end with [%s:%s]...' % (client[0], client[1]))
                link.sendall('Goodbye~'.encode())
                break
            print(f'{user_id}: {client_data}')
            # print('Client from [%s:%s] send a msg：%s' % (client[0], client[1], client_data))
        except Exception as e:
            print(e)
            print(f'Client from [{client[0]}:{client[1]}] has disconnected.')
            link.close()
            break
    # clients_list.pop(user_id) # remove from list when disconnected
    link.close()

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
        sys.exit(1)

    host, port = sys.argv[1:3]
    init_db()
    ip_port = (host, (int)(port))
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_STREAM is tcp
    sk.bind(ip_port)
    sk.listen(5)

    print('start socket server，waiting client...')
    
    while True:
        try:
            conn, address = sk.accept()
            print('New thread for [%s:%s]' % (address[0], address[1]))
            t = threading.Thread(target=link_handler, args=(conn, address))
            try:
                t.start()
            except Exception as e:
                print(f"Error occured: {e}")
        except KeyboardInterrupt:
            print("\nKeyboard interrupted, exiting...")
            break

if __name__=="__main__":
    main()