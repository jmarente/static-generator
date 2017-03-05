# -*- condig: utf-8 -*-
from generator.config import config


class FrontMatter(object):
    pass


class PageFactory(object):

    def get_pages(self, pages_folder, pages):
        return [Page(pages_folder, page) for page in pages]


class Page(object):
    content_path = None

    def __init__(self, folder, file):
        pass
