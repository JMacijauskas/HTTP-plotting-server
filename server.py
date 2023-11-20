import socket
import dataclasses
from typing import Optional

from Generators import color_generator
from Plotting import Plotter
from ProjectEnums import GraphPlot

SOCKET_ADDRESS = 'localhost'
SOCKET_PORT = 7789

PROTOCOL = b'HTTP/1.1'
TRANSFER_ENCODING = b'Transfer-Encoding: chunked'
OK_HEAD = b' '.join((PROTOCOL, b'200 OK'))
OK_MESSAGE = b'\r\n'.join((OK_HEAD, TRANSFER_ENCODING, b'', b'2', b'OK', b'0', b'\r\n'))
BAD_HEAD = b' '.join((PROTOCOL, b'400 BAD DATA'))
BAD_MESSAGE = b'\r\n'.join((BAD_HEAD, TRANSFER_ENCODING, b'', b'3', b'BAD', b'0', b'\r\n'))


@dataclasses.dataclass()
class Point:
    x: float
    y: float


class SimpleServer:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind((SOCKET_ADDRESS, SOCKET_PORT))
        self.socket.listen(5)
        self.graph = Plotter()
        self.color_generator = color_generator()

    def run(self) -> None:
        for color in self.color_generator:  # works as while loop, due to endless generator
            # accept connections from outside
            (client_socket, address) = self.socket.accept()
            print(f'Client ID: {address}, color: {color}')
            self.handle_client(client_socket, color)

    def handle_client(self, client_sock, client_color: str) -> None:
        while True:
            try:
                resquest_data, plot = self._listen_for_full_request(client_sock)
            except ConnectionResetError:
                break

            point = parse_data(resquest_data)
            if point:
                client_sock.sendall(OK_MESSAGE)
                self.graph.display_point(point.x, point.y, graph_type=plot, graph_color=client_color)
            else:
                client_sock.sendall(BAD_MESSAGE)

    @staticmethod
    def _listen_for_full_request(client_sock) -> tuple[bytes, Optional[GraphPlot]]:
        raw_response = client_sock.recv(4096)  # recv, for content length of bytes
        if not raw_response:
            raise ConnectionResetError
        body, missing_bytes, plot_type = parse_response(raw_response)
        if missing_bytes:
            body += client_sock.recv(missing_bytes)
        return body, plot_type


def parse_response(raw_data: bytes) -> tuple[bytes, int, Optional[GraphPlot]]:
    lagging_bytes = 0
    headers, data, *excess = raw_data.split(b'\r\n\r\n')

    headers_dict = parse_headers(headers)

    if 'Graph-Type' in headers_dict:
        try:
            plot_type = GraphPlot[headers_dict['Graph-Type']]
        except KeyError:
            print(f"Unsupported graph type: {headers_dict['Graph-Type']}. Regular plot will be used")
            plot_type = None
    else:
        plot_type = None

    if 'Content-Length' in headers_dict:
        data_length = int(headers_dict['Content-Length'])
    else:
        data_length = 0
    if len(data) != data_length:
        lagging_bytes = data_length
    return data, lagging_bytes, plot_type


def parse_data(raw_body: bytes) -> Optional[Point]:
    body = raw_body.decode('ASCII')
    if 'x=' in body and 'y=' in body:
        x_str, y_str, *_ = body.split('&')
        _, x = x_str.split('=')
        _, y = y_str.split('=')
        return Point(float(x.strip()), float(y.strip()))


def parse_headers(headers: bytes) -> dict[str, str]:
    headers_dict = {}
    for line in headers.decode('ASCII').splitlines():
        if ':' in line:
            header_name, value = line.split(':', 1)
            headers_dict[header_name] = value.strip()
    return headers_dict


if __name__ == '__main__':
    server = SimpleServer()
    server.run()
