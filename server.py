import socket
from typing import Optional
from collections import namedtuple
from Generators import color_generator
from Plotting import PeriodicPlotter
from ProjectEnums import GraphPlot
import threading
import numpy as np

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
        self.received_data = {}
        self.socket = socket.socket()
        self.socket.bind((SOCKET_ADDRESS, SOCKET_PORT))
        self.socket.listen(10)
        self.graph = PeriodicPlotter(self.received_data)
        self.color_generator = color_generator()

    def run(self) -> None:
        socket_thread = threading.Thread(name='Socket_wait', target=self.socket_func)
        print('Starting Socket_wait thread.')
        socket_thread.start()

        self.graph.cycle_display()  # renew with plotter

    def socket_func(self) -> None:
        for color in self.color_generator:  # works as while loop, due to endless generator
            # accept connections from outside
            (client_socket, address) = self.socket.accept()
            client_thread = threading.Thread(name=address[1], target=self.handle_client, args=(client_socket, address[1], color))
            print(f'Starting Client ID: {address}, color: {color} thread.')
            client_thread.start()

    def handle_client(self, client_sock: socket.socket, client_address: int, client_color: str) -> None:
        while True:
            try:
                request_data, plot = self._listen_for_full_request(client_sock)
            except ConnectionResetError:
                break

            point = parse_data(request_data)
            if point:
                client_sock.sendall(OK_MESSAGE)
                self.add_point(client_address, point.x, point.y, plot, client_color)
            else:
                client_sock.sendall(BAD_MESSAGE)

    @staticmethod
    def _listen_for_full_request(client_sock: socket.socket) -> tuple[bytes, Optional[GraphPlot]]:
        raw_response = client_sock.recv(4096)
        if not raw_response:
            raise ConnectionResetError
        body, missing_bytes, plot_type = parse_response(raw_response)
        if missing_bytes:
            body += client_sock.recv(missing_bytes)
        return body, plot_type

    def add_point(self, graph_id: int, x: float, y: float, graph_type: Optional[GraphPlot], graph_color: str):  # move to plotter
        if not graph_type:
            graph_type = GraphPlot.plot

        graph_axes = self.received_data.get(graph_id)
        if graph_axes:
            graph_data = graph_axes.get(graph_type.value)
            if graph_data:
                graph_data['x'] = np.append(graph_data['x'], [x])
                graph_data['y'] = np.append(graph_data['y'], [y])
            else:
                graph_axes[graph_type.value] = {'x': np.array([x]), 'y': np.array([y])}
        else:
            self.received_data[graph_id] = {graph_type.value: {'x': np.array([x]), 'y': np.array([y])}, 'color': graph_color}


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
