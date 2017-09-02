# -*- condig: utf-8 -*-
from sitic.content.paginable_content import PaginableContent


class Section(PaginableContent):

    def __init__(self, name, language):
        super(Section, self).__init__()
        self.name = name
        self.language = language

    def add_page(self, page):
        super(Section, self).add_page(page)
        page.section = self

    def set_content_page(self, page):
        self.content_page = page
        page.section = self

    def _get_url(self):
        url = '/'.join([self.name])
        # Section page might override section url
        if self.content_page and 'url' in self.content_page.frontmatter:
            url = self.content_page._get_url()
        return url

    def get_templates(self):
        return [
            "section/{}.html".format(self.name),
            "{}/section.html".format(self.name),
            "{}/list.html".format(self.name),
            "default/section.html",
            "default/list.html"
        ]

    @property
    def id(self):
        return self.name

    @property
    def title(self):
        title = self.format_string_to_title(self.name)
        if self.content_page and self.content_page.title != self.content_page.name:
            title = self.content_page.title
        return title

    @property
    def weight(self):
        weight=0
        if self.content_page:
            weight = self.content_page.weight
        return weight

    def get_plain_content(self):
        self.plain_content = ''
        if self.content_page:
            self.plain_content = self.content_page.get_plain_content()
        return self.plain_content

    def __repr__(self):
        return "Section: name «{}»".format(self.name)
