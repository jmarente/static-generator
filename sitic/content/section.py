# -*- condig: utf-8 -*-
from sitic.content.paginable_content import PaginableContent


class Section(PaginableContent):

    def __init__(self, name):
        super(Section, self).__init__()
        self.name = name

    def add_page(self, page):
        super(Section, self).add_page(page)
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

    def get_templates(self):
        return [
            "section/{}.html".format(self.name),
            "{}/section.html".format(self.name),
            "{}/list.html".format(self.name),
            "default/section.html",
            "default/list.html"
        ]
