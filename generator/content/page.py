# -*- condig: utf-8 -*-
import os

from generator.config import config


class Page(object):
    sections = []
    filename = ""
    name = ""
    frontmatter = {}
    content = ""

    def __init__(self, frontmatter, content, filename, sections = []):
        self.frontmatter = frontmatter or {}
        self.content = content or ""
        self.filename = filename or ""
        self.name = "_".join(self.filename.split('.')[0:-1])
        self.sections = sections or []

    def __getattr__(self, attribute):
        value = getattr(self, attribute) if hasattr(self, attribute) \
                else self.frontmatter.get(attribute, None)
        return value

    def get_url(self):
        alternative_url = self.sections + [self.name]
        url = self.frontmatter.get('url', None) or '/'.join(alternative_url)
        print('url', url)
        return url
