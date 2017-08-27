# -*- condig: utf-8 -*-
import os
import json
import shutil

from sitic.config import config

class Search(object):

    INDEX_FILE_NAME = 'sitic-search-index.js'
    FILES_TO_COPY = ['lunr.js', 'search.js']

    def __init__(self):
        self.index = []
        self.contents = []

    def add_contents(self, contents):
        self.contents += contents

    def get_index(self):

        for content in self.contents:
            content_context = content.get_context()
            get_plain_content = getattr(content, 'get_plain_content', None)
            page_index = {
                'title': content_context['title'],
                'url': content.get_url(),
                'content': get_plain_content() if callable(get_plain_content) else '',
                'language': content.language,
            }

            self.index.append(page_index)

        return self.index

    def get_path(self):
        url = self.get_url().split('/')
        path = os.path.join(config.public_path, *url)

        return path

    def get_url(self):
        parts = [self.INDEX_FILE_NAME]

        url = '/'.join(parts)

        url = '/' + url.lstrip('/')

        return url

    def create_files(self):
        index = self.get_index()
        with open(self.get_path(), 'w') as outfile:
            json.dump(index, outfile)

        for f in self.FILES_TO_COPY:
            file_path = os.path.join(config.files_path, f)
            target_path = os.path.join(config.public_path, f)
            shutil.copyfile(file_path, target_path)

    def get_html_includes(self):
        includes = []

        for f in self.FILES_TO_COPY:
            includes.append('<script src="/{}"></script>'.format(f))

        return includes
