# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from .utils import normalize_choices


class Structure(object):
    def __init__(self, fields=None):
        self.fields = fields or []

    def __add__(self, other):
        if other is None:
            return Structure(fields=self.fields)
        return Structure(fields=self.fields + other.fields)

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        return '<{}: fields=[{}]>'.format(
            self.__class__.__name__,
            ', '.join([field.name for field in self.fields]),
        )

    @classmethod
    def merge(klass, *structures):
        fields = []
        for structure in structures:
            if structure:
                fields += structure.fields
        return Structure(fields=fields)


class Field(object):
    def __init__(
        self, name, type, choices=None,
        label='', required=False, default=None, help_text=''
    ):
        self.name = name
        self.type = type
        self.choices = normalize_choices(choices)
        self.label = label
        self.required = required
        self.default = default
        self.help_text = help_text
