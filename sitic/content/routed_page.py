# -*- condig: utf-8 -*-
import os
from datetime import datetime
from collections import defaultdict

import lxml.html
import markdown
import textile
from docutils import core
from jinja2.utils import Markup

from sitic.utils import boolean, get_valid_date, constants
from sitic.config import config
from sitic.content.base_page import BasePage


class RoutedPage(BasePage):

    def _get_url(self):
        url = self.frontmatter.get('url', None)
        return url

    def get_templates(self):
        templates = []
        page_type = self.frontmatter.get('type', None)
        template_name = self.frontmatter.get('template', None)

        if template_name:
            if page_type:
                templates.append('{}/{}.html'.format(page_type, template_name))
            templates.append('{}/{}.html'.format(self.section.name, template_name))

        if page_type:
            templates.append("{}/routed_page.html".format(page_type))

        templates += [
            "{}/routed_page.html".format(self.section.name),
            "default/routed_page.html",
        ]

        return templates

    def __repr__(self):
        return "Routed page: title «{}» | url «{}» | section «{}»"\
                .format(self.title, self.get_url(), self.section.name)
