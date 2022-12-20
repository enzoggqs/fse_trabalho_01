from threading import Thread
import socket
import json

def connection_thread(con):
    while True:
        try:
            msg = con.recv(1024).decode('ascii')
            if not msg: break
            json_acceptable_string = msg.replace("'", "\"")
            d = json.loads(json_acceptable_string)
            print(d)
        except ValueError:
            print("Decoding JSON has failed")

def config_socket(tcp_ip_address, tcp_port):
    global connections

    print("Initalizing socket...")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (tcp_ip_address, tcp_port)
    tcp.bind(orig)
    tcp.listen(1)

    return tcp
    
    while True:
        con, client = tcp.accept()
        connections.append(con)
        print(con)
        print(connections)
        read_message_thread = Thread(target=connection_thread, args=(con,))
        read_message_thread.start()

def send_message(message):
    global connections
    print(message)
    if len(connections) > 0:
        for c in connections:
            c.send(json.dumps(message).encode())

def init_socket(tcp_ip_address, tcp_port):
    global connections

    print("Initalizing socket...")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (tcp_ip_address, tcp_port)
    tcp.bind(orig)
    tcp.listen(1)

    return tcp

