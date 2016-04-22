# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from collections import OrderedDict
import inspect
import re

from rest_framework.fields import empty, Field as SerializerField
from rest_framework.relations import RelatedField
from django_filters.filters import Filter as DjangoFilterField

from .documents import Document
from .resources import Action, Request, Resource, Response
from .structures import Field, Structure
from .types import get_raw_type
from .utils import (
    get_accept_media_types,
    get_allowed_methods,
    get_filter_class,
    get_filter_fields,
    get_response_status,
    get_serializer_class,
    get_serializer_fields,
    get_views,
    is_api_view,
)


URL_PARAMETER_PATTERN = re.compile(r'{(?P<param>.+?)}')


def create_document_from_urlpatterns(urlpatterns, **kwargs):
    document = Document(**kwargs)
    document.resources = [
        create_resource_from_api_view(url, view)
        for url, view in get_views(urlpatterns).items()
        if is_api_view(view)
    ]
    return document


def create_resource_from_api_view(path, view):
    document = inspect.getdoc(view.cls)

    resource = Resource(
        path=path,
        document=document or '',
        parameters=create_structure_from_path(path),
    )

    resource.actions = [
        create_action_from_api_view(resource, method, view)
        for method in get_allowed_methods(view.cls)
    ]

    return resource


def create_action_from_api_view(resource, method, view):
    document = inspect.getdoc(getattr(view.cls, method.lower()))

    serializer_class = get_serializer_class(view.cls)
    filter_class = get_filter_class(view.cls)
    parameters = create_structure_from_filter_class(filter_class)

    action = Action(
        resource=resource,
        method=method,
        document=document or '',
        parameters=parameters,
    )

    if method.lower() == 'get':
        request_attribute = None
    else:
        request_attribute = create_structure_from_serializer_class(
            serializer_class,
            only_writable=True,
        )
    action.requests = [
        Request(
            action=action,
            media_type=media_type,
            attribute=request_attribute,
        )
        for media_type in get_accept_media_types(view.cls)
    ]

    response_attribute = create_structure_from_serializer_class(
        serializer_class,
        only_readable=True,
    )
    action.responses = [
        Response(
            action=action,
            media_type='application/json',
            attribute=response_attribute,
            status=get_response_status(method, view.cls),
        ),
    ]

    return action


def create_structure_from_serializer_class(
    serializer_class,
    only_readable=False,
    only_writable=False,
):
    fields = create_fields_from_serializer_class(
        serializer_class,
        only_readable,
        only_writable,
    )
    if len(fields) == 0:
        return None
    return Structure(fields=fields)


def create_structure_from_filter_class(filter_class):
    fields = create_fields_from_filter_class(filter_class)
    if len(fields) == 0:
        return None
    return Structure(fields=fields)


def create_structure_from_path(path):
    params = URL_PARAMETER_PATTERN.findall(path)
    if len(params) == 0:
        return None

    return Structure(fields=[
        Field(name=param, type='number', required=True)  # TODO: Resolve type
        for param in params
    ])


# TODO: Hack me
def create_fields_from_serializer_class(
    serializer_class,
    only_readable=False,
    only_writable=False,
):
    if serializer_class is None:
        return []

    fields = get_serializer_fields(serializer_class)

    if only_readable:
        fields = OrderedDict([
            (name, field)
            for name, field in fields.items()
            if field.read_only or not field.write_only
        ])

    if only_writable:
        fields = OrderedDict([
            (name, field)
            for name, field in fields.items()
            if field.write_only or not field.read_only
        ])

    if len(fields) == 0:
        return []

    fields = [
        create_field_from_serializer_field(name, field)
        for name, field in fields.items()
    ]

    if only_readable:
        for index, field in enumerate(fields):
            fields[index].required = True

    return fields


def create_fields_from_filter_class(filter_class):
    if filter_class is None:
        return []

    fields = get_filter_fields(filter_class)
    if len(fields) == 0:
        return []

    return [
        create_field_from_filter_field(name, field)
        for name, field in fields.items()
    ]


def create_field_from_serializer_field(name, field):
    if not isinstance(field, SerializerField):
        raise TypeError('The arguemnt is not rest_framework.fields.Field')

    if not isinstance(field, RelatedField):
        choices = getattr(field, 'choices', None)
    else:
        choices = None

    default = field.default
    if issubclass(default, empty) or not default:
        default = ''

    return Field(
        name=name,
        type=get_raw_type(field),
        choices=choices,
        label=field.label or '',
        required=field.required,
        default=default,
        help_text=field.help_text or '',
    )


def create_field_from_filter_field(name, field):
    if not isinstance(field, DjangoFilterField):
        raise TypeError('The arguemnt is not django_filters.filters.Filter')

    # TODO: Ignore queryset choices
    choices = getattr(field.field, 'choices', None)

    help_text = field.field.help_text
    if help_text == 'Filter' or not help_text:
        help_text = ''

    return Field(
        name=name,
        type=get_raw_type(field),
        choices=choices,
        label=field.label or '',
        required=field.required,
        default=field.field.initial,
        help_text=help_text,
    )
