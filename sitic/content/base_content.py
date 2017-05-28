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
    _url = None
    url_file = 'index.html'

    def is_paginable(self):
        return self.paginable

    def _get_url(self):
        raise NotImplementedError()

    def get_url(self):
        if not self._url:
            url = self._get_url().strip('/')

            language_slug = ''
            if self.language:
                parts = [self.language] + url.split('/')
                url = '/'.join(parts)

            url = '/' + url.lstrip('/')

            self._url = url

        return self._url

    def absolute_url(self):
        url = self.get_url()

        return '/'.join([config.base_url.rstrip('/'), url.lstrip('/')])

    def get_simple_context(self):
        self.simple_context = {}
        self.simple_context['name'] = self.name
        self.simple_context['url'] = self.get_url()
        self.simple_context['absolute_url'] = self.absolute_url()
        return self.simple_context

    def get_context(self):
        self.context = self.get_simple_context()
        return self.context

    def to_publish(self):
        return True

    def is_expired(self):
        return False

    def get_base_path(self):
        url = self.get_url().split('/')
        path = os.path.join(config.public_path, *url)

        return path

    def get_path(self):
        index_path = os.path.join(self.get_base_path(), self.url_file)
        return index_path

    def get_templates(self):
        raise NotImplementedError()

    def __repr__(self):
        return "<%s instance at %s>" % (self.__class__.__name__, id(self))
