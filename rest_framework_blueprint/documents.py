# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function


class Document(object):
    def __init__(self, base_url, title, description=''):
        self.base_url = base_url
        self.title = title
        self.description = description
        self.resources = []
