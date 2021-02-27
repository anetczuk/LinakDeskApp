
import threading
import logging

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse

_LOGGER = logging.getLogger(__name__)

class LinakHTTPServer:

    def __init__(self, connector):
        self.connector = connector
        self.http_server = None

    def attachConnector(self, connector):
        _LOGGER.info("Attached connector to the http server")
        self.connector = connector
        DeskHTTPRequestHandler.desk = self.connector

    def run(self, port):
        # Add a http server
        DeskHTTPRequestHandler.desk = self.connector
        # handler = DeskHTTPRequestHandler(('127.0.0.1', 8000))
        self.http_server = HTTPServer(('127.0.0.1', port), DeskHTTPRequestHandler)

        def serve_forever(http_server):
            with http_server:  # to make sure httpd.server_close is called
                http_server.serve_forever()

        self.thread = threading.Thread(target=serve_forever, args=(self.http_server,))
        self.thread.setDaemon(True)
        self.thread.start()
        _LOGGER.info( "HTTP Server started on port %d", port )

    def stop(self):
        if self.http_server is not None:
            self.http_server.shutdown()
            self.http_server.socket.close()

class DeskHTTPRequestHandler(BaseHTTPRequestHandler):

    desk = None

    def __set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        _LOGGER.info("HTTP Server get called with " + str(self.path))
        instruction = parse.urlparse(self.path)
        self.__parse_instruction(instruction)
        self.__set_response()
        self.wfile.write(b'Called with instructions')

    def __parse_instruction(self, instruction):
        parts = instruction.path.split('/')
        if len(parts) != 3:
            raise ValueError('Expected two parts')

        if 'fave' == parts[1]:
            self.__do_execute_favourite(parts[2])
            return True
        else:
            raise ValueError('Unknown instruction ' + parts[0])

    def __do_execute_favourite(self, fave):
        _LOGGER.info("Favourite called with index " + str(fave))
        self.desk.moveToFav(int(fave))
        return True
