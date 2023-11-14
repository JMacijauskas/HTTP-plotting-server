import socket
import time
from typing import Optional

from Plotting import Plotter

SOCKET_ADDRESS = 'localhost'
SOCKET_PORT = 7789

PROTOCOL = b'HTTP/1.1'
TRANSFER_ENCODING = b'Transfer-Encoding: chunked'
OK_HEAD = b' '.join((PROTOCOL, b'200 OK'))
OK_MESSAGE = b'\r\n'.join((OK_HEAD, TRANSFER_ENCODING, b'', b'2', b'OK', b'0', b'\r\n'))
BAD_HEAD = b' '.join((PROTOCOL, b'400 BAD DATA'))
BAD_MESSAGE = b'\r\n'.join((BAD_HEAD, TRANSFER_ENCODING, b'', b'3', b'BAD', b'0', b'\r\n'))


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

    def handle_client(self, client_sock):
        while True:
            try:
                print(raw_response := self._listenForFullRequest(client_sock, 5))
            except ConnectionResetError:
                break
            if not raw_response:
                break
            response = parse_response(raw_response)
            if response['x'] is not None and response['y'] is not None:
                client_sock.sendall(OK_MESSAGE)
                self.graph.display_point(int(response['x']), int(response['y']))
            else:
                client_sock.sendall(BAD_MESSAGE)

    @staticmethod
    def _listenForFullRequest(client_sock, timeout: int) -> bytes:
        end_time = time.time() + timeout
        raw_response = b''
        while time.time() < end_time:
            if not raw_response.endswith(b'\r\n\r\n'):
                raw_response += client_sock.recv(4096)  # recv, for content length of bytes

            else:
                break
        return raw_response


def parse_response(raw_data: bytes) -> dict[str, Optional[str]]:
    for line in raw_data.decode('ASCII').splitlines():
        if 'x=' in line and 'y=' in line:
            x_str, y_str, *_ = line.split('&')
            _, x = x_str.split('=')
            _, y = y_str.split('=')
            resp_dict['x'] = x
            resp_dict['y'] = y


def parse_data(data: bytes):
    resp_dict = {'x': None, 'y': None}
    return resp_dict


if __name__ == '__main__':
    server = SimpleServer()
    server.run()
