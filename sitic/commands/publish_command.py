# -*- condig: utf-8 -*-
import os
import sys
import datetime

import click

from sitic.config import config
from sitic.utils.constants import DATE_FORMATS
from sitic.logging import logger
from sitic.content.frontmatter_handlers import TomlHandler
from sitic.content import page_parser


class PublishCommand(object):

    def __init__(self, filepath):
        self.filepath = filepath

        self.full_path = os.path.join(config.content_path, self.filepath)
        if not os.path.isfile(self.full_path):
            logger.error('File {} does no exists'.format(self.filepath))
            sys.exit(1)

    def run(self):
        frontmatter, content = page_parser.load(self.full_path)

        if not frontmatter.get('draft', False):
            logger.info('Content not marked as draft')
        else:
            frontmatter['draft'] = False

        if frontmatter.get('publication_date', None):
            answer = click.prompt('Would you like to update publication date?[Y/y]')
            if answer.lower() == 'y':
                frontmatter['publication_date'] = datetime.datetime.now().strftime(DATE_FORMATS[0])
        else:
            frontmatter['publication_date'] = datetime.datetime.now().strftime(DATE_FORMATS[0])

        toml_handler = TomlHandler()
        file_content = toml_handler.DELIMITER + os.linesep \
                + toml_handler.dump(frontmatter) + os.linesep \
                + toml_handler.DELIMITER + os.linesep + os.linesep \
                + content.strip()

        with open(self.full_path, 'w+') as f:
            f.write(file_content)
