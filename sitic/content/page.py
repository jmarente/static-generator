# -*- condig: utf-8 -*-
import os
import markdown

from sitic.config import config
from jinja2.utils import Markup


class Page(object):
    sections = []
    filename = ""
    name = ""
    frontmatter = {}
    content = ""
    context = {}

    def __init__(self, frontmatter, content, filename, sections = []):
        self.frontmatter = frontmatter or {}
        self.content = content or ""
        self.filename = filename or ""
        self.name = "_".join(self.filename.split('.')[0:-1])
        self.sections = sections or []

    def __getattr__(self, attribute):
        return self.frontmatter.get(attribute, None)

    def get_url(self):
        alternative_url = self.sections + [self.name]
        url = self.frontmatter.get('url', None) or '/'.join(alternative_url)
        return url

    @property
    def section(self):
        return self.sections[0] if len(self.sections) else None

    def get_context(self):
        if not self.context:
            self.context = dict(self.frontmatter)
            self.context['content'] = Markup(markdown.markdown(self.content))
            self.context['raw'] = self.content
        return self.context
