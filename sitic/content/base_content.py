# -*- condig: utf-8 -*-
import os
from copy import deepcopy

from six.moves.urllib import parse

from sitic.config import config

class BaseContent(object):
    name = ""
    paginable = False
    indexable = True
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

            if self.language and (self.language != config.main_language or not config.main_language_as_root):
                parts = [self.language] + url.split('/')
                url = '/'.join(parts)

            url = '/' + url.lstrip('/')

            self._url = url

        return self._url

    def has_redirect_url(self):
        return self.get_redirect_url() is not None

    def get_redirect_url(self):
        redirect_url = None
        if self.language and self.language == config.main_language:
            redirect_url = self._get_url().strip('/')
            if config.main_language_as_root:
                parts = [self.language] + redirect_url.split('/')
                redirect_url = '/'.join(parts)
            redirect_url = '/' + redirect_url.lstrip('/')
        return redirect_url


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
        self.context = deepcopy(self.get_simple_context())
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

    def format_string_to_title(self, string):
        string = string.replace('-', ' ')
        string = string.replace('_', ' ')
        return string.title()
