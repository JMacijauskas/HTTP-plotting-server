import socket
from typing import Optional

from Plotting import Plotter

SOCKET_ADDRESS = 'localhost'
SOCKET_PORT = 7789

PROTOCOL = b'HTTP/1.1'
RESPONSE_OK = b'200 OK'
RESPONSE_BAD = b'400 BAD DATA'


class SimpleServer:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind((SOCKET_ADDRESS, SOCKET_PORT))
        self.socket.listen(5)
        self.graph = Plotter()

    def run(self):
        while True:
            # accept connections from outside
            (client_socket, address) = self.socket.accept()
            print(raw_response := client_socket.recv(4096))
            response = parse_response(raw_response)
            if response['x'] is not None and response['y'] is not None:
                client_socket.send(PROTOCOL + b' ' + RESPONSE_OK)
                self.graph.display_point(int(response['x']), int(response['y']))
            else:
                client_socket.send(PROTOCOL + b' ' + RESPONSE_BAD)
            client_socket.close()


def parse_response(raw_data: bytes) -> dict[str, Optional[str]]:
    resp_dict = {'x': None, 'y': None}
    for line in raw_data.decode('ASCII').splitlines():
        if 'x=' in line and 'y=' in line:
            x_str, y_str, *_ = line.split('&')
            _, x = x_str.split('=')
            _, y = y_str.split('=')
            resp_dict['x'] = x
            resp_dict['y'] = y
    return resp_dict


if __name__ == '__main__':
    server = SimpleServer()
    server.run()
