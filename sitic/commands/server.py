# -*- condig: utf-8 -*-

import sys
import os
import posixpath
import argparse
from multiprocessing import Process

from six.moves import SimpleHTTPServer, socketserver

from sitic.generator import Generator
from sitic.commands.watcher import Watcher
from sitic.config import config
from sitic.logging import logger

class Server(object):

    def __init__(self, port):
        self.generator = Generator()
        self.watcher = Watcher()
        self.port = port

    def start(self):
        self.generator.gen()

        server_process = Process(target = self.start_server)
        watcher_process = Process(target = self.start_watcher)

        server_process.start()
        watcher_process.start()
        server_process.join()
        watcher_process.join()

    def start_server(self):

        config.public_path
        self.port

        os.chdir(config.public_path)

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", self.port), Handler)

        logger.info("Serving at: localhost:{}".format(self.port))

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info('Stopping server...')

        httpd.server_close()

    def start_watcher(self):
        self.watcher.start(generate_on_start=False)
