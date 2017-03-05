# -*- condig: utf-8 -*-
import os
import sys

import yaml

from generator.utils.singleton import Singleton
from generator.utils import constants


class _Config(metaclass=Singleton):
    config = None
    verbose = False
    port = None
    base_path = None
    content_path = None
    public_path = None
    extra_params = {}

    def load_config(self, config_file_path):
        self.config = config_file_path

        self.base_path = os.path.dirname(os.path.abspath(self.config))

        # Default
        self.content_path = os.path.join(self.base_path, constants.DEFAULT_CONTENT_PATH)
        self.public_path = os.path.join(self.base_path, constants.DEFAULT_PUBLIC_PATH)

        path_options = ['public_path', 'content_path']
        with open(self.config, 'r') as config_file:
            parsed_config = yaml.load(config_file)

            print('parsed_config', parsed_config)
            for param in parsed_config:
                if param in path_options:
                    value = parsed_config[param]
                    value = value if os.path.isdir(value) else os.path.join(self.base_path, value)
                    setattr(self, param, value)

        if not os.path.isdir(self.content_path):
            # TODO: throw error correctly
            raise Exception('No valid content path')
            sys.exit(1)


config = _Config()
