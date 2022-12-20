from threading import Thread
import os
import time
import sys
import central_socket
import json

connections = []
addresses = {}

def connection_thread(con):
    while True:
        try:
            msg = con.recv(1024).decode('ascii')
            if not msg: break
            json_acceptable_string = msg.replace("'", "\"")
            d = json.loads(json_acceptable_string)
        except ValueError:
            print("Decoding JSON has failed")

def start_menu():
    try:
        print('\nMenu Iniciado\n')
        print('-----------------\n')
        print('Escolha uma das seguintes opções:\n')
        print('M - Monitorar estados do sistema')
        aux = input('\nDigite a opção escolhida\n')
        if(aux == 'M'):
            st = ("Buscar estados")
            st = st.encode()
            print('tudo certo')
            print(type(socket))
            socket.send(st)
    except KeyboardInterrupt:
        quit()       
           
def connect():
    try:
        while True:
            con, client = socket.accept()
            print("Accepted a connection request from %s:%s"%(client[0], client[1]));
            con.send("Hello Client".encode())
            connections.append(con)
            read_message_thread = Thread(target=connection_thread, args=(con,))
            read_message_thread.start()
            print('entrou nes', connections)
            # addresses.append(addr[0])
            # listconn[addr[0]] = conn
    except RuntimeError as error:
        return error.args[0]

if __name__ == '__main__':
    try:
        tcp_ip_address = "164.41.98.26"
        tcp_port = 10059
        socket = central_socket.init_socket(tcp_ip_address, tcp_port)
        menu = Thread(target=start_menu)
        menu.start()
        allow_connections = Thread(target = connect)
        allow_connections.start()
    except KeyboardInterrupt:
        exit()