# -*- condig: utf-8 -*-
import os

from generator.config import config
from generator.content import PageFactory

class Generator(object):
    pages = []
    def __init__(self):
        page_factory = PageFactory()
        for root, directory, files in os.walk(config.content_path):
            print(root, directory, files)
            supported_files = [os.path.join(root, f) for f in files if f.endswith('.md')]
            self.pages += page_factory.get_pages(supported_files)

    def generate():
        pass
