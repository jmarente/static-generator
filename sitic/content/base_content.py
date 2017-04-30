# -*- condig: utf-8 -*-
import os

from six.moves.urllib import parse

from sitic.config import config

class BaseContent(object):
    name = ""
    paginable = False
    template_fields = ['name']
    simple_context = None
    context = None
    language = None

    def is_paginable(self):
        return self.paginable

    def _get_url(self):
        raise NotImplementedError()

    def get_url(self):
        url = self._get_url()

        language_slug = ''
        if self.language:
            url = parse.urljoin(language, url)

        return url

    url = property(get_url)

    def get_simple_context(self):
        raise NotImplementedError()

    def get_context(self):
        raise NotImplementedError()

    def to_publish(self):
        return True

    def is_expired(self):
        return False

    def get_base_path(self):
        url = self.get_url().split('/')
        path = os.path.join(config.public_path, *url)

        return path

    def get_path(self):
        index_path = os.path.join(self.get_base_path(), 'index.html')
        return index_path

    def get_templates(self):
        raise NotImplementedError()
