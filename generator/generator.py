# -*- condig: utf-8 -*-
import os
import shutil

from generator.config import config
from generator.content import PageFactory
from generator.utils import constants
from generator.template import Render

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

        self.create_public_folder()
        self.move_static_folder()

        for page in self.pages:
            page_path = self.create_page_folder(page)

            self.render.render(page, page_path)

    def create_public_folder(self):
        if not os.path.exists(config.public_path):
            os.makedirs(config.public_path)

    def move_static_folder(self):
        if os.path.exists(config.static_path):
            shutil.copytree(config.static_path, config.public_path)


    def create_page_folder(self, page):
        url = page.get_url().split('/')
        path = os.path.join(config.public_path, *url)

        if len(url) > 0:
            try:
                os.makedirs(path)
            except FileExistsError:
                pass

        index_path = os.path.join(path, 'index.html')

        open(index_path, 'a').close()
        return index_path
