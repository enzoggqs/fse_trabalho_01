import socket
import json
from threading import Thread, Event

def config_socket(config_file, tcp_ip_address, tcp_port):
    global connection
    global message
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (tcp_ip_address, tcp_port)
    connection.connect(dest)
    try:
        print('Conexão com servidor central estabelecida')
        st=str({"type": "new_connection", "config_file": config_file})
        byt=st.encode()
        connection.send(byt)
        while True:
            msg_rec = connection.recv(2048).decode('ascii')
            print(msg_rec)
        
    except socket.error as e:
        print(e)
        connection.close()

# def get_message():
    

def init_socket(config_file, tcp_ip_address, tcp_port):
    socket_thread = Thread(target=config_socket, args=(config_file,tcp_ip_address, tcp_port))
    socket_thread.start()
