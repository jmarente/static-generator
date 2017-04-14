# -*- condig: utf-8 -*-
import os

from sitic.config import config

class BaseContent(object):
    name = ""
    paginable = False
    template_fields = ['name']
    default_template_name = 'default'

    def is_paginable(self):
        return self.paginable

    def get_url(self):
        raise NotImplementedError()

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
        templates = []

        for field in self.template_fields:
            value = getattr(self, field, None)
            if not value:
                continue
            templates.append("{}.html".format(value))

        if self.default_template_name:
            templates.append("{}.html".format(self.default_template_name))

        return templates
