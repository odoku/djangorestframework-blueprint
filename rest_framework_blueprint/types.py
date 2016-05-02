# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import inspect

from django.utils.encoding import smart_text
from django_filters.filters import Filter as FilterField
from rest_framework.serializers import ListSerializer, ModelSerializer
from rest_framework.fields import Field as SerialzierField


TYPE_BOOLEAN = 'boolean'
TYPE_NUMBER = 'number'
TYPE_STRING = 'string'
TYPE_ARRAY = 'array'
TYPE_OBJECT = 'object'
TYPE_ENUM = 'enum'


TYPE_MAP = {
    'boolean':           TYPE_BOOLEAN,
    'checkbox':          TYPE_BOOLEAN,
    'nullboolean':       TYPE_BOOLEAN,
    'nullbooleanselect': TYPE_BOOLEAN,

    'integer': TYPE_NUMBER,
    'float':   TYPE_NUMBER,
    'decimal': TYPE_NUMBER,
    'number':  TYPE_NUMBER,

    'char':     TYPE_STRING,
    'text':     TYPE_STRING,
    'textarea': TYPE_STRING,
    'email':    TYPE_STRING,
    'password': TYPE_STRING,
    'url':      TYPE_STRING,
    'regex':    TYPE_STRING,
    'slug':     TYPE_STRING,
    'uuid':     TYPE_STRING,

    'time':     TYPE_STRING,
    'date':     TYPE_STRING,
    'datetime': TYPE_STRING,
    'duration': TYPE_STRING,

    'hidden':         TYPE_STRING,
    'multiplehidden': TYPE_STRING,
    'readonly':       TYPE_STRING,

    'file':          TYPE_STRING,
    'clearablefile': TYPE_STRING,
    'image':         TYPE_STRING,

    'choice':                 TYPE_STRING,
    'select':                 TYPE_STRING,
    'selectmultiple':         TYPE_STRING,
    'radioselect':            TYPE_STRING,
    'checkboxselectmultiple': TYPE_STRING,

    'list':  TYPE_ARRAY,
    'array': TYPE_ARRAY,

    'dict':  TYPE_OBJECT,
    'json':  TYPE_OBJECT,
    'model': TYPE_OBJECT,
}


def get_raw_type(field):
    if isinstance(field, SerialzierField):
        return get_raw_type_from_serializer_field(field)

    if isinstance(field, FilterField):
        return get_raw_type_from_filter_field(field)

    return smart_text(field.__name__).lower()


def get_raw_type_from_serializer_field(field):
    if isinstance(field, ListSerializer):
        return 'list'

    if isinstance(field, ModelSerializer):
        return 'model'
        # return smart_text(field.Meta.model.__name__).lower()

    name = field.__class__.__name__

    if name.endswith('Field'):
        name = smart_text(name[:-5])

    return smart_text(name).lower()


def get_raw_type_from_filter_field(field):
    if inspect.isclass(field.widget):
        name = field.widget.__name__
    else:
        name = field.widget.__class__.__name__

    if name.endswith('Input'):
        name = smart_text(name[:-5])

    elif name.endswith('Widget'):
        name = smart_text(name[:-6])

    return smart_text(name).lower()


def get_mson_type(raw_type):
    return TYPE_MAP.get(raw_type, 'string')
