# -*- condig: utf-8 -*-
import os

import lxml.html
import markdown
import textile
from docutils import core
from jinja2.utils import Markup

from sitic.utils import constants
from sitic.config import config
from sitic.content.base_page import BasePage


class Page(BasePage):
    content = ""
    relative_path = []
    template_fields = ['template', 'type', 'section', 'name']

    def __init__(self, frontmatter, content, name, extension, file_path, relative_path = [], language = None, section = None):
        self.content = content or ""
        self.name = name
        self.relative_path = relative_path
        self.file_path = file_path
        self.extension = extension

        self.html_content = ''
        self.plain_content = ''

        super(Page, self).__init__(frontmatter, language, section)

    def _get_url(self):
        alternative_url = self.relative_path + [self.name]
        url = self.frontmatter.get('url', None) or '/'.join(alternative_url)
        return url

    def get_context(self):
        if self.context is None:
            self.context = super(Page, self).get_context()
            self.context['content'] = Markup(self.get_html_content())
            self.context['raw_content'] = self.content
        return self.context

    def get_html_content(self):
        if not self.html_content:
            extension = '.' + self.extension.lstrip('.')
            if extension in constants.TEXTILE_EXTENSIONS:
                self.html_content = textile.textile(self.content)
            elif extension in constants.REESTRUCTURED_TEXT_EXTENSIONS:
                self.html_content = core.publish_parts(self.content, writer_name='html')['html_body']
            else:
                self.html_content = markdown.markdown(self.content)
        return self.html_content

    def get_plain_content(self):
        if not self.plain_content and self.get_html_content():
            self.plain_content = lxml.html.fromstring(self.get_html_content()).text_content()
        return self.plain_content

    @property
    def id(self):
        page_id = self.frontmatter.get('id', None)
        if not page_id:
            paths = self.relative_path + [self.name]
            page_id = '-'.join(paths)
        return page_id

    @property
    def title(self):
        return self.frontmatter.get('title', self.name)

    def get_description(self):
        if not self.description:
            if not self.frontmatter.get('description', None):
                plain_content = self.get_plain_content()
                self.description = plain_content[0:config.description_length]
                if len(plain_content) > config.description_length:
                    self.description += '...'
            else:
                self.description = self.frontmatter.get('description')

        return self.description

    def get_templates(self):
        templates = []
        page_type = self.frontmatter.get('type', None)
        template_name = self.frontmatter.get('template', None)

        if template_name:
            if page_type:
                templates.append('{}/{}.html'.format(page_type, template_name))
            templates.append('{}/{}.html'.format(self.section.name, template_name))

        if page_type:
            templates.append("{}/page.html".format(page_type))

        templates += [
            "{}/page.html".format(self.section.name),
            "default/page.html",
        ]

        return templates

    def __repr__(self):
        return "Content page: title «{}» | url «{}» | path «{}»"\
                .format(self.title, self.get_url(), self.relative_path)
