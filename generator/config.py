# -*- condig: utf-8 -*-
from generator.utils.singleton import Singleton


class _Config(metaclass=Singleton):
    config = None
    port = None

    def load_config(self, config_file_path):
        self.config = config_file_path

    def set_port(self, port):
        self.port = port


Config = _Config()
