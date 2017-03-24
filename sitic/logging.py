#-*- encoding: utf-8 -*-
import logging


class ColorFormatter(logging.Formatter):

    def color(self, level=None):
        codes = {\
            None:       (1,   0),
            'DEBUG':    (1,   32), # verde
            'INFO':     (1,   36), # cian
            'WARNING':  (1,  33), # amarillo
            'ERROR':    (1,  31), # rojo
            'CRITICAL': (1, 101), # blanco, fondo rojo
            }
        return (chr(27)+'[%d;%dm') % codes[level]

    def format(self, record):
        start_color = self.color(record.levelname)
        end_color = self.color()
        return "{}{}{}: {}".format(start_color, record.levelname, end_color, record.getMessage())


class _Logger(object):

    def __init__(self):
        self.logger = logging.getLogger('Sitic')
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(ColorFormatter())

        self.logger.addHandler(handler)

    def debug(self, text):
        self.logger.debug(text)

    def info(self, text):
        self.logger.info(text)

    def warning(self, text):
        self.logger.warning(text)

    def error(self, text):
        self.logger.error(text)

    def critical(self, text):
        self.logger.critical(text)

logger = _Logger()
