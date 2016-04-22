# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from collections import OrderedDict
from importlib import import_module
import re

from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.utils.encoding import smart_text
from django.utils.module_loading import import_string
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.views import APIView


URL_PARAMETER_PATTERN = re.compile(r'(<(?P<param>.+?)>)')


def get_urlpatterns():
    try:
        urlconf = import_string(settings.ROOT_URLCONF)
    except ImportError:
        urlconf = import_module(settings.ROOT_URLCONF)

    if hasattr(urlconf, 'urls'):
        return urlconf.urls.urlpatterns
    return urlconf.urlpatterns


def get_views(urlpatterns, base=''):
    views = OrderedDict()
    for pattern in urlpatterns:
        if isinstance(pattern, RegexURLResolver):
            views.update(get_views(
                urlpatterns=pattern.url_patterns,
                base=base + pattern.regex.pattern,
            ))
        elif isinstance(pattern, RegexURLPattern):
            url = base + pattern.regex.pattern
            url = URL_PARAMETER_PATTERN.sub('{\g<param>}', simplify_regex(url))
            views[url] = pattern.callback
    return views


def is_api_view(view):
    return hasattr(view, 'cls') and issubclass(view.cls, APIView)


def get_serializer_class(view_class):
    try:
        return view_class().get_serializer_class()
    except Exception:
        return getattr(view_class, 'serializer_class', None)


def get_serializer_fields(serializer_class):
    instance = serializer_class()
    return instance.fields


def get_filter_class(view_class):
    # TODO: Get from filter backend class
    return getattr(view_class, 'filter_class', None)


def get_filter_fields(filter_class):
    instance = filter_class()
    return instance.filters


def get_allowed_methods(view_class):
    return [
        smart_text(method).upper()
        for method in view_class.http_method_names
        if hasattr(view_class, method) and method != 'options'
    ]


def get_accept_media_types(view_class):
    return [
        parser.media_type
        for parser in view_class().get_parsers()
    ]


def get_response_status(method, view_class):
    method = method.upper()
    if method == 'POST' and issubclass(view_class, CreateModelMixin):
        return status.HTTP_201_CREATED

    if method == 'DELETE' and issubclass(view_class, DestroyModelMixin):
        return status.HTTP_204_NO_CONTENT

    return status.HTTP_200_OK


def normalize_choices(choices):
    if isinstance(choices, (list, tuple)):
        return OrderedDict(choices)
    return choices
