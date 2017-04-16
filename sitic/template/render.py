# -*- condig: utf-8 -*-
import os
import inspect

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from sitic.config import config
from sitic.template import filters

class Render(object):
    environment = None
    loader = None
    def __init__(self):
        self.loader = FileSystemLoader(config.templates_path)
        self.environment = Environment(loader=self.loader)

        for name, function in inspect.getmembers(filters, predicate=inspect.isfunction):
            self.environment.filters[name] = function

    def render(self, content, output_path, context):
        template = self.get_content_template(content)
        if template:
            template.stream(**context).dump(output_path)

    def get_content_template(self, content):
        template = None
        possible_templates = content.get_templates()

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
