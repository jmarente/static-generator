# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent

class PaginableContent(BaseContent):
    paginable = True

    def __init__(self):
        self.pages = []
        self.content_page = None
        self.rss = None

    def get_pages(self):
        return sorted(self.pages, key=lambda x: x.get_publication_date(), reverse=True)

    def add_page(self, page):
        if page not in self.pages:
            self.pages.append(page)

    def set_rss(self, rss):
        if not self.rss or self.rss != rss:
            self.rss = rss

    def get_simple_context(self):
        if self.simple_context is None:
            pages = self.get_pages()
            self.simple_context = super(PaginableContent, self).get_simple_context()
            self.simple_context['page_count'] = len(self.pages)
            if len(pages):
                self.simple_context['modification_date'] = pages[0].modification_date
            if self.content_page:
                self.simple_context['page'] = self.content_page.get_simple_context()
                del self.simple_context['page']['url']
        return self.simple_context

    def get_context(self):
        if self.context is None:
            self.context = super(PaginableContent, self).get_context()
            self.context['pages'] = [p.get_simple_context() for p in self.pages]
            if self.content_page:
                self.context['page'] = self.content_page.get_context()
        return self.context
