from threading import Thread
import os
import time
import sys
import distributed_socket

if __name__ == '__main__':
    try:
        config_file = 'configuracao_sala_02.json'
        tcp_ip_address = "164.41.98.26"
        tcp_port = 10055
        distributed_socket.init_server(config_file)

    except KeyboardInterrupt:
        exit()
