# -*- condig: utf-8 -*-

import sys
import os
import posixpath
import argparse
from multiprocessing import Process

from six.moves import SimpleHTTPServer, socketserver, BaseHTTPServer
from six.moves.urllib import parse

from sitic.generator import Generator
from sitic.watcher import Watcher
from sitic.config import config
from sitic.logging import logger

INDEXFILE = 'index.html'


class HttpServer(SimpleHTTPServer.HTTPServer):

    def __init__(self, base_path, *args, **kwargs):
        SimpleHTTPServer.HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path


class HttpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def translate_path(self, path):
        dth = posixpath.normpath(parse.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path


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

        Handler = HttpHandler

        httpd = HttpServer(config.public_path, ("", self.port), HttpHandler)

        logger.info("Serving at: localhost:{}".format(self.port))

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info('Stopping server...')

        httpd.server_close()

    def start_watcher(self):
        self.watcher.start(generate_on_start=False)
