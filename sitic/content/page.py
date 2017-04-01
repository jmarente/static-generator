# -*- condig: utf-8 -*-
import os
from datetime import datetime

import markdown
from jinja2.utils import Markup

from sitic.utils import boolean, get_valid_date
from sitic.config import config
from sitic.content.base_content import BaseContent


class Page(BaseContent):
    sections = []
    filename = ""
    frontmatter = {}
    content = ""
    context = {}
    draft = False
    publication_date = None
    expiration_date = None

    def __init__(self, frontmatter, content, filename, sections = []):
        self.frontmatter = frontmatter or {}
        self.content = content or ""
        self.filename = filename or ""
        self.name = "_".join(self.filename.split('.')[0:-1])
        self.sections = sections or []

        self.draft = boolean(self.frontmatter.pop('draft', None))
        self.taxonomies = []

        date_fields = ['publication_date', 'expiration_date']
        for field in date_fields:
            value = get_valid_date(self.frontmatter.pop(field, None), None)
            setattr(self, field, value)

    def __getattr__(self, attribute):
        return self.frontmatter.get(attribute, None)

    def get_url(self):
        alternative_url = self.sections + [self.name]
        url = self.frontmatter.get('url', None) or '/'.join(alternative_url)
        return url

    @property
    def section(self):
        return self.sections[0] if len(self.sections) else None

    def get_simple_context(self):
        return dict(self.frontmatter)

    def get_context(self):
        if not self.context:
            self.context = self.get_simple_context()
            self.context['content'] = Markup(markdown.markdown(self.content))
            self.context['raw_content'] = self.content
        return self.context

    def to_publish(self):
        to_publish = True
        now = datetime.now()

        if not config.build_draft and self.draft:
            to_publish = False
        elif not config.build_future \
                and self.publication_date  \
                and self.publication_date > now:
            to_publish = False
        elif self.is_expired():
            to_publish = False

        return to_publish

    def is_expired(self):
        now = datetime.now()
        return not config.build_expired \
                and self.expiration_date \
                and self.expiration_date <= now

    def get_path(self):
        url = self.get_url().split('/')
        path = os.path.join(config.public_path, *url)

        index_path = os.path.join(path, 'index.html')
        return index_path
