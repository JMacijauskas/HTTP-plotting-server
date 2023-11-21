import socket
from typing import Optional
from collections import namedtuple
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


Point = namedtuple("Point", "x y")


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
            self.handle_client(client_socket, address[1], color)

    def handle_client(self, client_sock, client_address: int, client_color: str) -> None:
        while True:
            try:
                resquest_data, plot = self._listen_for_full_request(client_sock)
            except ConnectionResetError:
                break

            point = parse_data(resquest_data)
            if point:
                client_sock.sendall(OK_MESSAGE)
                self.graph.display_point(point.x, point.y, graph_id=client_address, graph_type=plot, graph_color=client_color)
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

    plot_type = headers_dict.get('Graph-Type')
    if plot_type:
        plot_type = GraphPlot[plot_type]

    data_length = headers_dict.get('Content-Length', 0)
    if data_length:
        data_length = int(data_length)

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
