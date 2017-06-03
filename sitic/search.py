# -*- condig: utf-8 -*-
import os
import json

from sitic.config import config

class Search(object):

    INDEX_FILE_NAME = 'sitic-search-index.js'

    def __init__(self, language, contents):
        self.language = language
        self.contents = contents
        self.index = []

    def get_index(self):

        for content in self.contents:
            content_context = content.get_context()
            page_index = {
                'title': content_context['title'],
                'url': content.get_url(),
                'content': content.get_plain_content(),
            }

            self.index.append(page_index)

        return self.index

    def get_path(self):
        url = self.get_url().split('/')
        path = os.path.join(config.public_path, *url)

        return path

    def get_url(self):
        parts = [self.INDEX_FILE_NAME]

        if self.language:
            parts = [self.language] + parts

        url = '/'.join(parts)

        url = '/' + url.lstrip('/')

        return url

    def create_file(self):
        index = self.get_index()
        with open(self.get_path(), 'w') as outfile:
            json.dump(index, outfile)
