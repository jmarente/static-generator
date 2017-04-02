# -*- condig: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from sitic.config import config

class Render(object):
    environment = None
    loader = None
    def __init__(self):
        self.loader = FileSystemLoader(config.templates_path)
        self.environment = Environment(loader=self.loader)

    def render(self, page, output_path, context):
        template = self.get_page_template(page)
        if template:
            template.stream(**context).dump(output_path)

    def get_page_template(self, page):
        template = None
        possible_templates = page.get_templates()

        for template_name in possible_templates:
            template = self.get_template(template_name)
            if template:
                break;

        return template

    def get_template(self, template_name):
        try:
            template = self.environment.get_template(template_name)
        except TemplateNotFound as e:
            template = None
        return template
