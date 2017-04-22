# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent


class Section(BaseContent):
    paginable = True
    content_page = None

    def __init__(self, name):
        self.name = name
        self.pages = []

    def add_page(self, page):
        if page not in self.pages:
            self.pages.append(page)
            page.section = self

    def set_content_page(self, page):
        self.content_page = page
        page.section = self

    def get_url(self):
        url = '/'.join([self.name])
        # Section page might override section url
        if self.content_page and 'url' in self.content_page.frontmatter:
            url = self.content_page.get_url()
        return url

    def get_simple_context(self):
        if self.simple_context is None:
            self.simple_context = {
                'name': self.name,
                'page_count': len(self.pages),
                'url': self.get_url(),
            }
            if self.content_page:
                self.simple_context['page'] = self.content_page.get_simple_context()
                del self.simple_context['page']['url']
        return self.simple_context

    def get_context(self):
        if self.context is None:
            self.context = self.get_simple_context()
            self.context['pages'] = [p.get_simple_context() for p in self.pages]
            if self.content_page:
                self.context['page'] = self.content_page.get_context()
        return self.context

    def get_templates(self):
        return [
            "section/{}.html".format(self.name),
            "{}/section.html".format(self.name),
            "{}/list.html".format(self.name),
            "default/section.html",
            "default/list.html"
        ]
