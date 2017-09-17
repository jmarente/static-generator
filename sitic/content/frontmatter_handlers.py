# -*- condig: utf-8 -*-
import re
import json

import yaml
import toml

try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper
    from yaml import SafeLoader



class BaseHandler(object):
    DELIMITER = None
    CHAR_DELIMITER = None
    RE_DELIMITER = None

    def __init__(self, delimiter=None):
        self.CHAR_DELIMITER = delimiter or self.CHAR_DELIMITER

        regex = self.RE_DELIMITER or '^\%s{3,}$' % self.CHAR_DELIMITER
        self.RE_DELIMITER = re.compile(regex, re.MULTILINE)

    def has_format(self, text):
        return self.RE_DELIMITER.match(text) is not None

    def split(self, text):
        _, data, content = self.RE_DELIMITER.split(text)
        return data, content

    def load(self, text):
        raise NotImplementedError

    def dump(self, data):
        raise NotImplementedError


class YamlHander(BaseHandler):
    CHAR_DELIMITER = '-'
    DELIMITER = '---'
    RE_DELIMITER = "^-{3,}$"

    def load(self, text):
        return yaml.load(text)

    def dump(self, data):
        kwargs = {}
        kwargs.setdefault('Dumper', SafeDumper)
        kwargs.setdefault('default_flow_style', False)

        metadata = yaml.dump(data, **kwargs).strip()
        return metadata


class TomlHandler(BaseHandler):
    CHAR_DELIMITER = '+'
    DELIMITER = '+++'
    RE_DELIMITER = "^\+{3,}$"

    def load(self, text):
        return toml.loads(text)

    def dump(self, data):
        metadata = toml.dumps(data).strip()
        return metadata
