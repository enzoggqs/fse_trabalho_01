from threading import Thread
import os
import time
import sys
from datetime import datetime
import central_socket
import json
import pickle
import csv

HEADERSIZE = 512

connections = {}
connected_rooms = []

def generate_log(msg):
    with open('../log.sv', 'a') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',')
        print(datetime.now().strftime('%d/%m/%Y %H:%M')+' - ',msg,file = csvfile)
        

def connection_thread(con):
    while True:
        full_msg = b''
        new_msg = True
        while True:
            msg = con.recv(4096)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
            full_msg += msg

            if len(full_msg)-HEADERSIZE == msglen:

                d = pickle.loads(full_msg[HEADERSIZE:])
                print(d)

                new_msg = True
                full_msg = b''

def start_menu():
    try:
        print('\nMenu Iniciado\n')
        print('-----------------\n')
        print('Escolha uma das seguintes opções:\n')
        print('0 - Sair do programa')
        print('1 - Monitorar estados de entrada e saída do sistema')
        print('2 - Monitorar temperatura e humidade do sistema')
        print('3 - Ligar/Desligar dispositivos')
        print('4 - Listar conexões')

        aux = input('\nDigite a opção escolhida\n')
        if(aux == '0'):
            print('entrou aq')
            sys.exit()
        if(aux == '1'):
            st = ("op1")
            st = st.encode()
            connections[connected_rooms[0]].send(st)

            time.sleep(3)

            generate_log(f'Gera novos dados para monitoramento')
        
            start_menu()
        if(aux == '2'):
            try:
            # stop = input('A temperatura e a umidade serão mostradas e atualizadas a cada 2s. Pressione qualquer tecla para voltar ao menu')
                # time.sleep(2)
                st = ("op2")
                st = st.encode()
                connections[connected_rooms[0]].send(st)

                generate_log(f'Busca valores de temperatura e umidade da sala')

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
            print('5 - Alarme')
            print('6 - Todos os de saída')
            disp = input("\nDigite a opção escolhida\n")
            while(disp != '1' and disp != '2' and disp != '3' and disp != '4'and disp != '5' and disp != '6'):
                disp = input("\nDigite a opção escolhida\n")
            st += str(disp)
            choice = input("Você deseja LIGAR(1) ou DESLIGAR(0)")
            while(choice != '1' and choice != '0'):
                choice = input("Você deseja LIGAR(1) ou DESLIGAR(0)")

            if(choice == 1 and disp != 6):
                generate_log(f'Liga dispositivo')
            if(choice == 2 and disp != 6):
                generate_log(f'Desliga dispositivo')
            if(choice == 1 and disp == 6):
                generate_log(f'Liga todos os dispositivo')
            if(choice == 2 and disp != 6):
                generate_log(f'Desliga todos os dispositivo')

            st += str(choice)
            st = st.encode()
            connections[connected_rooms[0]].send(st)

        
            start_menu()
        if(aux == '4'):
            print(connections)
            print(connected_rooms)
            rooms = []
            for room in connected_rooms:
                if(room[-2:] == '15'):
                    rooms.append('Sala 4')
                if(room[-2:] == '28'):
                    rooms.append('Sala 3')
                if(room[-2:] == '26'):
                    rooms.append('Sala 2')
                if(room[-2:] == '29'):
                    rooms.append('Sala 1')
            print(rooms)

            generate_log(f'Lista Salas')

    except KeyboardInterrupt:
        quit()       
           
def connect():
    try:
        while True:
            con, client = socket.accept()
            print("Accepted a connection request from %s:%s"%(client[0], client[1]));
            connected_rooms.append(client[0])
            connections[client[0]] = con
            read_message_thread = Thread(target=connection_thread, args=(con,))
            read_message_thread.start()
            connections[connected_rooms[0]] = con 
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
        # while(True):
        #     if(menu.is_alive() == False):
        #         KeyboardInterrupt
        #     time.sleep(1)
    except KeyboardInterrupt:
        exit()