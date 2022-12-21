import socket
import json
import RPi.GPIO as GPIO
from threading import Thread, Event
import pickle
import board
import adafruit_dht

HEADERSIZE = 512

# L_01 = 26
# L_02 = 19
# AC = 13
# PR = 6
# AL_BZ = 5
# SPres = 0
# SFum = 11
# SJan = 9
# SPor = 10
# SC_IN = 22
# SC_OUT = 27

states = {
    'L_01': [26, 'Desligado', 'Lâmpada 1'],
    'L_02': [19, 'Desligado', 'Lâmpada 2'],
    'AC': [13, 'Desligado', 'Ar Condicionado'],
    'PR': [6, 'Desligado', 'Projetor'],
    'AL_BZ': [5, 'Desligado', 'Alarme'],
    'SPres': [0, 'Desligado', 'Sensor de Presença'],
    'SFum': [11, 'Desligado', 'Sensor de Fumaça'],
    'SJan': [9, 'Desligado', 'Sensor de Janela'],
    'SPor': [10, 'Desligado', 'Sensor de Porta'],
    'Pessoas': ['', 0, 'Número de Pessoas'],
    'Temperatura': ['', 0, 'Temperatura'],
    'Umidade': ['', 0, 'Umidade'],
}

def config_socket(config_file, tcp_ip_address, tcp_port):
    global connection
    global message
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (tcp_ip_address, tcp_port)
    connection.connect(dest)
    try:
        st={"type": "new_connection", "config_file": config_file}
        byt = pickle.dumps(st)
        byt = bytes(f'{len(byt):<{HEADERSIZE}}', 'utf-8') + byt
        connection.send(byt)
        while True:
            msg_rec = connection.recv(2048).decode('ascii')
            print(msg_rec)
            if(msg_rec[0:3] == "op1"):
                msg = threat_states()
                msg = pickle.dumps(msg)

                msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
                connection.send(msg)
            elif(msg_rec[0:3] == "op2"):
                print('op2 entrou')
                device = adafruit_dht.DHT22(board.D18, False)
                msg = {"Temperatura": device.temperature, "Umidade": device.humidity}
                msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
                connection.send(msg)
            elif(msg_rec[0:3] == "op3"):
                turning_on_thread = Thread(target=turn_on_outputs, args=(msg_rec[3], msg_rec[4]))
                turning_on_thread.start()


    except socket.error as e:
        print(e)
        connection.close()

def setup_pins():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(states['L_01'][0], GPIO.OUT)
        GPIO.setup(states['L_02'][0], GPIO.OUT)
        GPIO.setup(states['AC'][0], GPIO.OUT)
        GPIO.setup(states['PR'][0], GPIO.OUT)
        GPIO.setup(states['AL_BZ'][0], GPIO.OUT)
        GPIO.setup(states['SPres'][0], GPIO.IN)
        GPIO.setup(states['SFum'][0], GPIO.IN)
        GPIO.setup(states['SJan'][0], GPIO.IN)
        GPIO.setup(states['SPor'][0], GPIO.IN)
        GPIO.setup(22, GPIO.IN)
        GPIO.setup(27, GPIO.IN)
    except RuntimeError as error:
        return error.args[0]

def update_states():
    setup_pins()

    if(GPIO.input(states['L_01'][0])):
        states['L_01'][1] = 'Ligado'
    else:
        states['L_01'][1] = 'Desligado'
    if(GPIO.input(states['L_02'][0])):
        states['L_02'][1] = 'Ligado'
    else:
        states['L_02'][1] = 'Desligado'
    if(GPIO.input(states['AC'][0])):
        states['AC'][1] = 'Ligado'
    else:
        states['AC'][1] = 'Desligado'
    if(GPIO.input(states['PR'][0])):
        states['PR'][1] = 'Ligado'
    else:
        states['PR'][1] = 'Desligado'
    if(GPIO.input(states['AL_BZ'][0])):
        states['AL_BZ'][1] = 'Ligado'
    else:
        states['AL_BZ'][1] = 'Desligado'
    if(GPIO.input(states['SPres'][0])):
        states['SPres'][1] = 'Ligado'
    else:
        states['SPres'][1] = 'Desligado'
    if(GPIO.input(states['SFum'][0])):
        states['SFum'][1] = 'Ligado'
    else:
        states['SFum'][1] = 'Desligado'
    if(GPIO.input(states['SJan'][0])):
        states['SJan'][1] = 'Ligado'
    else:
        states['SJan'][1] = 'Desligado'
    if(GPIO.input(states['SPor'][0])):
        states['SPor'][1] = 'Ligado'
    else:
        states['SPor'][1] = 'Desligado'  

def turn_on_outputs(option, choice):
    aux = True
    print(choice)
    if(choice == '0'):
        aux = False
    setup_pins()
    if(option == "1"):
        GPIO.output(states['L_01'][0], aux)
    if(option == "2"):
        GPIO.output(states['L_02'][0], aux)
    if(option == "3"):
        GPIO.output(states['AC'][0], aux)
    if(option == "4"):
        GPIO.output(states['PR'][0], aux)
    if(option == "5"):
        GPIO.output(states['L_01'][0], aux)
        GPIO.output(states['L_02'][0], aux)
        GPIO.output(states['AC'][0], aux)
        GPIO.output(states['PR'][0], aux)
        GPIO.output(states['AL_BZ'][0], aux)

def threat_states():
    update_states()
    new_dict = {}
    for el in states.values():
        new_dict[el[2]] = el[1]
    
    return new_dict

def init_socket(config_file, tcp_ip_address, tcp_port):
    socket_thread = Thread(target=config_socket, args=(config_file,tcp_ip_address, tcp_port))
    socket_thread.start()
