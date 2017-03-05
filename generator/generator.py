# -*- condig: utf-8 -*-
import os

from generator.config import config
from generator.page import PageFactory

class Generator(object):
    pages = []
    def __init__(self):
        for root, directory, files in os.walk(config.content_path):
            print(root, directory, files)
            supported_files = [f for f in files if f.endswith('.md')]
            pages += PageFactory.get_pages(directory)

    def generate():
        pass
