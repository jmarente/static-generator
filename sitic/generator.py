# -*- condig: utf-8 -*-
import os
import shutil

from sitic.config import config
from sitic.content import ContentFactory, Paginator
from sitic.content import MenuBuilder
from sitic.utils import constants
from sitic.template import Render
from sitic.logging import logger

class Generator(object):
    context = {}

    def __init__(self):
        self.content_factory = ContentFactory()
        for root, directory, files in os.walk(config.content_path):
            supported_files = [os.path.join(root, f) for f in files
                    if f.endswith(tuple(constants.VALID_CONTENT_EXTENSIONS))]
            self.content_factory.build_contents(supported_files)

    def gen(self):
        self.create_public_folder()
        self.move_static_folder()

        for language in config.get_languages():
            render = Render()

            contents = self.content_factory.get_contents(language)
            expired_contents = self.content_factory.expired_contents[language]

            taxonomies = self.content_factory.get_taxonomies(language)
            sections = self.content_factory.get_sections(language)

            homepage = self.content_factory.homepages[language]
            homepage.pages = contents

            menu_builder = MenuBuilder(contents, sections)

            menus = menu_builder.build()

            contents = [homepage] + contents + taxonomies + sections

            for content in contents:
                if content.is_paginable() and config.paginable:
                    self.generate_paginable(render, content)
                else:
                    self.generate_regular(render, content)

            self.remove_expired(expired_contents)

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

    def generate_regular(self, render, content):
        content_path = content.get_path()

        self.create_path(content_path)
        self.context['node'] = content.get_context()
        render.render(content, content_path, self.context)

    def generate_paginable(self, render, content):
        paginator = Paginator(content, config.paginable)
        for page_num in paginator.page_range:
            page = paginator.get_page(page_num)
            page_path = page.get_path()

            paginator.page = page

            self.create_path(page_path)
            self.context['node'] = content.get_context()
            self.context['paginator'] = paginator
            render.render(content, page_path, self.context)

    def remove_expired(self, expired_contents):
        for content in expired_contents:
            content_path = content.get_path()
            # Removes expired content previously published
            if content.is_expired() and os.path.isfile(content_path):
                os.remove(content_path)
