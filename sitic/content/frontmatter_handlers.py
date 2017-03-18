# -*- condig: utf-8 -*-
import re
import json

import yaml
import toml


class BaseHandler(object):
    DELIMITER = None
    RE_DELIMITER = None

    def __init__(self, delimiter=None):
        self.DELIMITER = delimiter or self.DELIMITER

        regex = self.RE_DELIMITER or '^\%s{3,}$' % self.DELIMITER
        self.RE_DELIMITER = re.compile(regex, re.MULTILINE)

    def has_format(self, text):
        return self.RE_DELIMITER.match(text) is not None

    def split(self, text):
        _, data, content = self.RE_DELIMITER.split(text)
        return data, content

    def load(self, text):
        raise NotImplementedError


class YamlHander(BaseHandler):
    DELIMITER = '-'
    RE_DELIMITER = "^-{3,}$"

    def load(self, text):
        return yaml.load(text)


class TomlHandler(BaseHandler):
    DELIMITER = '+'
    RE_DELIMITER = "^\+{3,}$"

    def load(self, text):
        return toml.loads(text)
