# -*- condig: utf-8 -*-
import os
import sys

import click
import yaml

from sitic.config import config
from sitic.utils.constants import VALID_CONTENT_EXTENSIONS
from sitic.logging import logger
from sitic.content.frontmatter_handlers import TomlHandler, YamlHander


class NewSiteCommand(object):

    def __init__(self, path):

        if os.path.isfile(path):
            logger.error('Not valid path, its a file')
            sys.exit(1)

        self.path = path

    def run(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        folders = ['content', 'layouts', 'static', 'data']

        for folder in folders:
            folder_path = os.path.join(self.path, folder)
            if os.path.exists(folder_path) and not os.path.isdir(folder_path):
                logger.error('content folder already exists and is not a folder')
                sys.exit(1)
            elif not os.path.exists(folder_path):
                os.mkdir(folder_path)

        routing_file_path = os.path.join(self.path, 'data/routing.json')
        if not os.path.exists(routing_file_path):
            with open(routing_file_path, 'w+') as routing_file:
                routing_file.write('[]')

        config_path = os.path.join(self.path, 'sitic.yml')
        config = {
            'title': 'My Sitic site',
            'base_url': 'www.example.org',
        }

        if not os.path.exists(config_path):
            with open(config_path, 'w+') as config_file:
                config_file.write(yaml.dump(config, default_flow_style=False))
