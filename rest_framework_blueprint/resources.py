# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function


class Resource(object):
    def __init__(self, path, document='', parameters=None, actions=None):
        self.path = path
        self.parameters = parameters
        self.document = document
        self.actions = actions or []

    def __repr__(self):
        return '<{}: {} {}>'.format(
            self.__class__.__name__,
            self.path,
        )


class Action(object):
    def __init__(
        self, resource, method,
        document='', parameters=None,
    ):
        self.resource = resource
        self.method = method
        self.document = document
        self.parameters = parameters
        self.requests = []
        self.responses = []

    def __repr__(self):
        return '<{}: {} {}>'.format(
            self.__class__.__name__,
            self.method,
            self.path,
        )


class Request(object):
    def __init__(
        self,
        action, media_type,
        headers=None, attribute=None, body=None,
    ):
        self.action = action
        self.media_type = media_type
        self.headers = headers
        self.attribute = attribute
        self.body = body


class Response(object):
    def __init__(
        self,
        action, media_type,
        headers=None, attribute=None, body=None,
        status=200,
    ):
        self.action = action
        self.media_type = media_type
        self.headers = headers
        self.attribute = attribute
        self.body = body
        self.status = status
