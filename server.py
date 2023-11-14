import socket
from typing import Optional

from Plotting import Plotter

SOCKET_ADDRESS = 'localhost'
SOCKET_PORT = 7789

PROTOCOL = b'HTTP/1.1'
RESPONSE_OK = b'200 OK'
OK_HEAD = b' '.join((PROTOCOL, RESPONSE_OK))
RESPONSE_BAD = b'400 BAD DATA'
BAD_HEAD = b' '.join((PROTOCOL, RESPONSE_BAD))
RESPONSE_CONTINUE = b'100-continue'
KEEP_ALIVE = b'Connection: keep-alive'


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
            self.handle_client(client_socket)
            # client_socket.close()

    def handle_client(self, client_sock):
        while True:
            print(raw_response := client_sock.recv(4096))
            if not raw_response:
                break
            response = parse_response(raw_response)
            if response['x'] is not None and response['y'] is not None:
                print(resp_message := b'\r\n'.join((OK_HEAD, b'Transfer-Encoding: chunked', b'', b'2', b'OK', b'0', b'\r\n')))
                client_sock.sendall(resp_message)
                self.graph.display_point(int(response['x']), int(response['y']))
            else:
                print(resp_message := b'\r\n'.join(
                    (BAD_HEAD, b'Transfer-Encoding: chunked', b'', b'3', b'BAD', b'0', b'\r\n')))
                client_sock.sendall(resp_message)


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
