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
    render = None
    def __init__(self):
        self.render = Render()
        page_factory = PageFactory()
        for root, directory, files in os.walk(config.content_path):
            supported_files = [os.path.join(root, f) for f in files
                    if f.endswith(tuple(constants.VALID_CONTENT_EXTENSIONS))]
            self.pages += page_factory.get_pages(supported_files)

    def gen(self):
        context = {}

        self.create_public_folder()
        self.move_static_folder()

        for page in self.pages:
            page_to_publish = page.to_publish()
            page_path = self.get_page_folder(page, build_path=page_to_publish)

            if page_to_publish:
                context['page'] = page.get_context()
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

    def get_page_folder(self, page, build_path=True):
        url = page.get_url().split('/')
        path = os.path.join(config.public_path, *url)

        if len(url) > 0 and build_path:
            try:
                os.makedirs(path)
            except FileExistsError:
                pass

        index_path = os.path.join(path, 'index.html')
        return index_path
