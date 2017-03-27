# -*- condig: utf-8 -*-
import os
import sys
import re

import yaml

from sitic.utils import constants
from sitic.logging import logger


class _Config():
    config = None
    verbose = False
    base_path = None
    content_path = None
    public_path = None
    static_path = None
    templates_path = None
    extra_params = {}
    ignore_files_regex = []
    build_draft = False
    build_future = False
    build_expired = False

    def load_config(self, config_file_path):
        self.config = config_file_path

        self.base_path = os.path.dirname(os.path.abspath(self.config))

        # Default
        self.content_path = os.path.join(self.base_path, constants.DEFAULT_CONTENT_PATH)
        self.public_path = os.path.join(self.base_path, constants.DEFAULT_PUBLIC_PATH)
        self.static_path = os.path.join(self.base_path, constants.DEFAULT_STATIC_PATH)
        self.templates_path = os.path.join(self.base_path, constants.DEFAULT_TEMPLATES_PATH)

        path_options = ['public_path', 'content_path', 'static_path']
        with open(self.config, 'r') as config_file:
            parsed_config = yaml.load(config_file)

            print('parsed_config', parsed_config)
            for param in parsed_config:
                if param in path_options:
                    value = parsed_config[param]
                    value = value if os.path.isabs(value) else os.path.join(self.base_path, value)
                    setattr(self, param, value)

        if not os.path.isdir(self.content_path):
            logger.error('Invalid path for content. Folder not found')
            sys.exit(1)

        # TODO: make patterns configurables
        self.ignore_files_regex = [re.compile(i) for i in constants.IGNORE_FILES_PATTERN]


config = _Config()
