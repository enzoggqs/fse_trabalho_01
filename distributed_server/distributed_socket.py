import socket
import json
import RPi.GPIO as GPIO
from threading import Thread, Event
import pickle
import board
import adafruit_dht
import time

HEADERSIZE = 512

states = {}

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

            if(msg_rec[0:3] == "op1"):
                msg = threat_states()
                msg = pickle.dumps(msg)

                msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
                connection.send(msg)

            elif(msg_rec[0:3] == "op2"):
                dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
                msg = {"Temperatura": dhtDevice.temperature, "Umidade": dhtDevice.humidity}
                msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
                connection.send(msg)

            elif(msg_rec[0:3] == "op3"):
                turn_on_outputs(msg_rec[3], msg_rec[4])

                if(msg_rec[4] == 0):
                    msg = "Dispositivo desligado com sucesso!"

                else:
                    msg = {"msg": "Dispositivo ligado com sucesso!"}
                    msg = pickle.dumps(msg)
                    msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
                    connection.send(msg)

    except socket.error as e:
        print(e)
        connection.close()

def setup_pins():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(states['L_01'][0][0], GPIO.OUT)
        GPIO.setup(states['L_02'][0][0], GPIO.OUT)
        GPIO.setup(states['AC'][0][0], GPIO.OUT)
        GPIO.setup(states['PR'][0][0], GPIO.OUT)
        GPIO.setup(states['AL_BZ'][0][0], GPIO.OUT)
        GPIO.setup(states['SPres'][0][0], GPIO.IN)
        GPIO.setup(states['SFum'][0][0], GPIO.IN)
        GPIO.setup(states['SJan'][0][0], GPIO.IN)
        GPIO.setup(states['SPor'][0][0], GPIO.IN)
        GPIO.setup(22, GPIO.IN)
        GPIO.setup(27, GPIO.IN)
    except RuntimeError as error:
        return error.args[0]

def update_states():
    setup_pins()

    while(True):
        if(GPIO.input(states['L_01'][0][0])):
            states['L_01'][0][1] = 'Ligado'
        else:
            states['L_01'][0][1] = 'Desligado'
        if(GPIO.input(states['L_02'][0][0])):
            states['L_02'][0][1] = 'Ligado'
        else:
            states['L_02'][0][1] = 'Desligado'
        if(GPIO.input(states['AC'][0][0])):
            states['AC'][0][1] = 'Ligado'
        else:
            states['AC'][0][1] = 'Desligado'
        if(GPIO.input(states['PR'][0][0])):
            states['PR'][0][1] = 'Ligado'
        else:
            states['PR'][0][1] = 'Desligado'
        if(GPIO.input(states['AL_BZ'][0][0])):
            states['AL_BZ'][0][1] = 'Ligado'
        else:
            states['AL_BZ'][0][1] = 'Desligado'
        if(GPIO.input(states['SPres'][0][0])):
            states['SPres'][0][1] = 'Ligado'
            spres_thread = Thread(target=presence_sensor_active,)
            spres_thread.start()
        else:
            states['SPres'][0][1] = 'Desligado'
        if(GPIO.input(states['SFum'][0][0])):
            states['SFum'][0][1] = 'Ligado'
            GPIO.output(states['AL_BZ'][0][0], True)
        else:
            states['SFum'][0][1] = 'Desligado'
        if(GPIO.input(states['SJan'][0][0])):
            states['SJan'][0][1] = 'Ligado'
        else:
            states['SJan'][0][1] = 'Desligado'
        if(GPIO.input(states['SPor'][0][0])):
            states['SPor'][0][1] = 'Ligado'
        else:
            states['SPor'][0][1] = 'Desligado' 
        time.sleep(0.01) 

def presence_sensor_active():
    GPIO.output(states['L_01'][0][0], True)
    GPIO.output(states['L_02'][0][0], True)
    time.sleep(15)
    GPIO.output(states['L_01'][0][0], False)
    GPIO.output(states['L_02'][0][0], False)

def turn_on_outputs(option, choice):
    aux = True
    if(choice == '0'):
        aux = False
    if(option == "1"):
        GPIO.output(states['L_01'][0][0], aux)
    if(option == "2"):
        GPIO.output(states['L_02'][0][0], aux)
    if(option == "3"):
        GPIO.output(states['AC'][0][0], aux)
    if(option == "4"):
        GPIO.output(states['PR'][0][0], aux)
    if(option == "5"):
        GPIO.output(states['AL_BZ'][0][0], aux)
    if(option == "6"):
        GPIO.output(states['L_01'][0][0], aux)
        GPIO.output(states['L_02'][0][0], aux)
        GPIO.output(states['AC'][0][0], aux)
        GPIO.output(states['PR'][0][0], aux)
        GPIO.output(states['AL_BZ'][0][0], aux)

def threat_states():
    new_dict = {}
    for el in states.values():
        # print(el[0][2])
        new_dict[el[0][2]] = el[0][1]
    
    return new_dict

def count_people():
    people_amount = 0
    setup_pins()
    while(True):
        states['Pessoas'][0][1] = people_amount
        if GPIO.input(22):
            people_amount = people_amount + 1
        if GPIO.input(27):
            people_amount = people_amount - 1
            if(people_amount < 0):
                people_amount = 0
        time.sleep(0.05)

def handle_states():

    people_thread = Thread(target=count_people, )
    people_thread.start()
    update_states_thread = Thread(target=update_states, )
    update_states_thread.start()

    # with open(config_file,'r') as aux_file:
    # obj = json.load(aux_file)
    # state[]

def init_server(config_file):
    with open(config_file,'r') as aux_file:
        aux = json.load(aux_file)

        tcp_ip_address = aux['ip_servidor_central']
        tcp_port = aux['porta_servidor_central']

        states['L_01'] = [aux['outputs'][0]['gpio'], 'Desligado', 'Lâmpada 1'],
        states['L_02'] = [aux['outputs'][1]['gpio'], 'Desligado', 'Lâmpada 2'],
        states['AC'] = [aux['outputs'][3]['gpio'], 'Desligado', 'Ar Condicionado'],
        states['PR'] = [aux['outputs'][2]['gpio'], 'Desligado', 'Projetor'],
        states['AL_BZ'] = [aux['outputs'][4]['gpio'], 'Desligado', 'Alarme'],
        states['SPres'] = [aux['inputs'][0]['gpio'], 'Desligado', 'Sensor de Presença'],
        states['SFum'] = [aux['inputs'][1]['gpio'], 'Desligado', 'Sensor de Fumaça'],
        states['SJan'] = [aux['inputs'][2]['gpio'], 'Desligado', 'Sensor de Janela'],
        states['SPor'] = [aux['inputs'][3]['gpio'], 'Desligado', 'Sensor de Porta'],
        states['Pessoas'] =  ['', 0, 'Número de Pessoas'],
        
    time.sleep(2)

    socket_thread = Thread(target=config_socket, args=(config_file, tcp_ip_address, tcp_port))
    socket_thread.start()
    states_thread = Thread(target=handle_states)
    states_thread.start()
