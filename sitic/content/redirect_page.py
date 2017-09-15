# -*- condig: utf-8 -*-
import os

from sitic.content.base_content import BaseContent


class RedirectPage(BaseContent):

    def __init__(self, from_url, to_url):
        self.from_url = from_url
        self.to_url = to_url

    def get_url(self):
        return self.from_url

    def get_templates(self):
        return ['sitic_html_redirect.html']

    def get_context(self):
        return {
            'to_url': self.to_url,
            'from_url': self.from_url,
        }

    def __repr__(self):
        return "Redirect page: from_url «{}» | to_url «{}»" \
                .format(self.from_url, self.to_url)

    def get_redirect_url(self):
        return None
