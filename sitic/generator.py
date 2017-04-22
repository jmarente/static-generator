# -*- condig: utf-8 -*-
import os
import shutil

from sitic.config import config
from sitic.content import ContentFactory, Paginator
from sitic.utils import constants
from sitic.template import Render
from sitic.logging import logger

class Generator(object):
    contents = []
    sections = []
    taxonomies = []
    context = {}
    homepage = None
    render = None

    def __init__(self):
        self.render = Render()
        content_factory = ContentFactory()
        for root, directory, files in os.walk(config.content_path):
            supported_files = [os.path.join(root, f) for f in files
                    if f.endswith(tuple(constants.VALID_CONTENT_EXTENSIONS))]
            self.contents += content_factory.get_contents(supported_files)

        self.taxonomies = content_factory.get_taxonomies()
        self.sections = content_factory.get_sections()
        self.homepage = content_factory.homepage
        self.homepage.pages = self.contents

    def gen(self):
        self.create_public_folder()
        self.move_static_folder()

        contents = [self.homepage] + self.contents + self.taxonomies + self.sections

        for content in contents:
            content_to_publish = content.to_publish()

            if content_to_publish:
                if content.is_paginable() and config.paginable:
                    self.generate_paginable(content)
                else:
                    self.generate_regular(content)

            content_path = content.get_path()
            # Removes expired content previously published
            if content.is_expired() and os.path.isfile(content_path):
                os.remove(content_path)

        logger.info('Site generated')

    def create_public_folder(self):
        if not os.path.exists(config.public_path):
            os.makedirs(config.public_path)

    def move_static_folder(self):
        if os.path.exists(config.static_path):
            shutil.copytree(config.static_path, config.public_path)

    def create_path(self, content_path):
        path = os.path.dirname(content_path)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except FileExistsError as e:
                pass

    def generate_regular(self, content):
        content_path = content.get_path()

        self.create_path(content_path)
        self.context['node'] = content.get_context()
        self.render.render(content, content_path, self.context)

    def generate_paginable(self, content):
        paginator = Paginator(content, config.paginable)
        for page_num in paginator.page_range:
            page = paginator.get_page(page_num)
            page_path = page.get_path()

            paginator.page = page

            self.create_path(page_path)
            self.context['node'] = content.get_context()
            self.context['paginator'] = paginator
            self.render.render(content, page_path, self.context)
