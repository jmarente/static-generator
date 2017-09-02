# -*- condig: utf-8 -*-
import os
from math import ceil

import six

class Paginator(object):
    def __init__(self, content, per_page, orphans=0, allow_empty_first_page=True):
        self._num_pages = self._count = None
        self.page = None
        self.content = content
        self.object_list = content.get_pages()
        self.per_page = int(per_page) if int(per_page) > 0 else self._get_count()
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page

    def get_page(self, number):
        "Returns a Page object for the given 1-based page number."
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count

        objects_context = [o.get_simple_context() for o in self.object_list[bottom:top]]
        return Page(objects_context, number, self)

    def _get_count(self):
        "Returns the total number of objects, across all pages."
        if self._count is None:
                self._count = len(self.object_list)
        return self._count
    count = property(_get_count)

    def _get_num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            elif self.per_page < 1:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return range(1, self.num_pages + 1)
    page_range = property(_get_page_range)


class Page(object):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (slice,) + six.integer_types):
            raise TypeError
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        return list(self.object_list)[index]

    # The following four methods are only necessary for Python <2.6
    # compatibility (this class could just extend 2.6's collections.Sequence).

    def __iter__(self):
        i = 0
        try:
            while True:
                v = self[i]
                yield v
                i += 1
        except IndexError:
            return

    def __contains__(self, value):
        for v in self:
            if v == value:
                return True
        return False

    def index(self, value):
        for i, v in enumerate(self):
            if v == value:
                return i
        raise ValueError

    def count(self, value):
        return sum([1 for v in self if v == value])

    # End of compatibility methods.

    @property
    def has_next(self):
        return self.number < self.paginator.num_pages

    @property
    def has_previous(self):
        return self.number > 1

    @property
    def has_other_pages(self):
        return self.has_previous or self.has_next

    @property
    def next_number(self):
        return self.paginator.validate_number(self.number + 1)

    @property
    def previous_number(self):
        return self.paginator.validate_number(self.number - 1)

    @property
    def previous_url(self):
        url = ''
        if self.has_previous:
            previous_page = self.paginator.get_page(self.number - 1)
            url = previous_page.get_url()
        return url

    @property
    def next_url(self):
        url = ''
        if self.has_next:
            next_page = self.paginator.get_page(self.number + 1)
            url = next_page.get_url()
        return url

    @property
    def last_url(self):
        page = self.paginator.get_page(self.paginator.num_pages)
        return page.get_url()

    @property
    def first_url(self):
        page = self.paginator.get_page(1)
        return page.get_url()

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page

    def get_url(self):
        index = self.number
        url = self.paginator.content.get_url()
        if index != 1:
            url = '/'.join([url, 'page', str(index)])

        url = '/' + url.lstrip('/')

        return url
    url=property(get_url)

    def get_path(self):
        index = self.number
        base_path = self.paginator.content.get_base_path()
        path_parts = [base_path]
        if index != 1:
            path_parts += ['page', str(index)]
        path_parts.append('index.html')
        return os.path.join(*path_parts)
