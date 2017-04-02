# -*- condig: utf-8 -*-
import os
import shutil

from sitic.config import config
from sitic.content import PageFactory
from sitic.utils import constants
from sitic.template import Render
from sitic.logging import logger

class Generator(object):
    pages = []
    taxonomies = []
    render = None

    def __init__(self):
        self.render = Render()
        page_factory = PageFactory()
        for root, directory, files in os.walk(config.content_path):
            supported_files = [os.path.join(root, f) for f in files
                    if f.endswith(tuple(constants.VALID_CONTENT_EXTENSIONS))]
            self.pages += page_factory.get_pages(supported_files)

        self.taxonomies = list(page_factory.taxonomies.values())

    def gen(self):
        context = {}

        self.create_public_folder()
        self.move_static_folder()

        contents = self.pages + self.taxonomies

        for page in contents:
            page_to_publish = page.to_publish()
            page_path = page.get_path()

            if page_to_publish:
                self.create_path(page_path)
                context['node'] = page.get_context()
                self.render.render(page, page_path, context)

            # Removes expired content previously published
            if page.is_expired() and os.path.isfile(page_path):
                os.remove(page_path)

        logger.info('Site generated')

    def create_public_folder(self):
        if not os.path.exists(config.public_path):
            os.makedirs(config.public_path)

    def move_static_folder(self):
        if os.path.exists(config.static_path):
            shutil.copytree(config.static_path, config.public_path)

    def create_path(self, page_path):
        path = os.path.dirname(page_path)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except FileExistsError as e:
                pass
