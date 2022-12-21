from threading import Thread
import os
import time
import sys
import central_socket
import json
import pickle

HEADERSIZE = 512

connections = {}
addresses = []

def connection_thread(con):
    while True:
        full_msg = b''
        new_msg = True
        while True:
            msg = con.recv(4096)
            if new_msg:
                # print(f"new message length: {msg[:HEADERSIZE]}")
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
            full_msg += msg

            if len(full_msg)-HEADERSIZE == msglen:
                # print("full msg recvd")
                # print(full_msg[HEADERSIZE:])

                d = pickle.loads(full_msg[HEADERSIZE:])
                print(d)

                new_msg = True
                full_msg = b''
        # print(full_msg)
        # try:
        #     msg = con.recv(1024).decode('ascii')
        #     if not msg: break
        #     full_msg += msg
        #     d = json.loads(json_acceptable_string)
        #     print(d)
        # except ValueError:
        #     print("Decoding JSON has failed")

def start_menu():
    try:
        print('\nMenu Iniciado\n')
        print('-----------------\n')
        print('Escolha uma das seguintes opções:\n')
        print('0 - Sair do programa')
        print('1 - Monitorar estados de entrada e saída do sistema')
        print('2 - Monitorar temperatura e humidade do sistema')
        print('3 - Ligar/Desligar dispositivos')
        aux = input('\nDigite a opção escolhida\n')
        if(aux == '0'):
            quit()
        if(aux == '1'):
            st = ("op1")
            st = st.encode()
            connections[addresses[0]].send(st)

            time.sleep(3)
        
            start_menu()
        if(aux == '2'):
            try:
            # stop = input('A temperatura e a umidade serão mostradas e atualizadas a cada 2s. Pressione qualquer tecla para voltar ao menu')
                # time.sleep(2)
                st = ("op2")
                st = st.encode()
                connections[addresses[0]].send(st)

                time.sleep(10)

                start_menu()

            except RuntimeError as error:
                return error.args[0]
        if(aux == '3'):
            st = "op3"
            print("Qual dispositivo deseja ligar/desligar?")
            print('1 - Lâmpada 01')
            print('2 - Lâmpada 02')
            print('3 - Ar Condicionado')
            print('4 - Projetor')
            print('5 - Todos os de saída')
            disp = input("\nDigite a opção escolhida\n")
            while(disp != '1' and disp != '2' and disp != '3' and disp != '4'and disp != '5'):
                disp = input("\nDigite a opção escolhida\n")
            st += str(disp)
            choice = input("Você deseja LIGAR(1) ou DESLIGAR(0)")
            while(choice != '1' and choice != '0'):
                choice = input("Você deseja LIGAR(1) ou DESLIGAR(0)")
            st += str(choice)
            st = st.encode()
            connections[addresses[0]].send(st)

        
            start_menu()

    except KeyboardInterrupt:
        quit()       
           
def connect():
    try:
        while True:
            con, client = socket.accept()
            print("Accepted a connection request from %s:%s"%(client[0], client[1]));
            addresses.append(client[0])
            connections[client[0]] = con
            read_message_thread = Thread(target=connection_thread, args=(con,))
            read_message_thread.start()
            connections[addresses[0]] = con 
    except RuntimeError as error:
        return error.args[0]

if __name__ == '__main__':
    try:
        tcp_ip_address = "164.41.98.26"
        tcp_port = 10055
        socket = central_socket.init_socket(tcp_ip_address, tcp_port)
        menu = Thread(target=start_menu)
        menu.start()
        allow_connections = Thread(target = connect)
        allow_connections.start()
    except KeyboardInterrupt:
        exit()