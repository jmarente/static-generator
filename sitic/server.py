# -*- condig: utf-8 -*-

import sys
import os
from multiprocessing import Process

from six.moves import SimpleHTTPServer, socketserver
from six.moves.urllib import parse

from sitic.generator import Generator
from sitic.watcher import Watcher
from sitic.config import config
from sitic.logging import logger

INDEXFILE = 'index.html'

class HttpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):

        # Parse query data to find out what was requested
        parsedParams = parse.urlparse(self.path)

        # See if the file requested exists
        if os.access('.' + os.sep + parsedParams.path, os.R_OK):
            # File exists, serve it up
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        else:
            # send index.html, but don't redirect
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open(INDEXFILE, 'rb') as fin:
                self.copyfile(fin, self.wfile)


class Server(object):

    def __init__(self, port):
        self.generator = Generator()
        self.watcher = Watcher()
        self.port = port

    def start(self):
        self.generator.gen()

        os.chdir(config.public_path)

        # self.start_server()

        server_process = Process(target = self.start_server)
        watcher_process = Process(target = self.start_watcher)

        server_process.start()
        watcher_process.start()
        server_process.join()
        watcher_process.join()

    def start_server(self):

        Handler = HttpHandler

        httpd = socketserver.TCPServer(("", self.port), Handler)

        logger.info("Serving at: localhost:{}".format(self.port))

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info('Stopping server...')

    def start_watcher(self):
        self.watcher.start(generate_on_start=False)
