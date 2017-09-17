# -*- condig: utf-8 -*-
import os
import sys

import click

from sitic.config import config
from sitic.utils.constants import VALID_CONTENT_EXTENSIONS
from sitic.logging import logger
from sitic.content.frontmatter_handlers import TomlHandler, YamlHander


class NewCommand(object):

    def __init__(self, filepath, title, frontmatter_format):
        self.filepath = filepath
        self.title = title
        self.frontmatter_format = frontmatter_format

        parts = os.path.split(self.filepath)
        self.filename = parts[-1]
        self.path = parts[0:-1]

        valid_extension = False
        for extension in VALID_CONTENT_EXTENSIONS:
            if self.filename.endswith(extension):
                valid_extension = True
                break

        if not valid_extension:
            logger.error('Not valid file extesion, valid ones: {}'
                         .format(', '.join(VALID_CONTENT_EXTENSIONS)))
            sys.exit(1)

        full_path = os.path.join(config.content_path, self.filepath)
        if os.path.isfile(full_path):
            logger.error('File {} already exists'.format(self.filepath))
            sys.exit(1)

        while not self.title:
            self.title = click.prompt('Please enter a title', default=None, type=str)

    def run(self):
        paths = config.content_path
        for folder in self.path:
            paths = os.path.join(paths, folder)
            if not os.path.isdir(paths):
                os.mkdir(paths)

        frontmatter_handler = TomlHandler() if self.frontmatter_format == 'toml' else YamlHander()

        metadata = {
            'title': self.title,
            'draft': True,
        }

        file_content = frontmatter_handler.DELIMITER + os.linesep \
                + frontmatter_handler.dump(metadata) + os.linesep \
                + frontmatter_handler.DELIMITER + os.linesep + os.linesep

        full_path = os.path.join(config.content_path, self.filepath)
        with open(full_path, 'w+') as f:
            f.write(file_content)
