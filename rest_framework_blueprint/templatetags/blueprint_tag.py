# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django import template
from django.template.loader import render_to_string

from rest_framework_blueprint.resources import Action, Request, Resource, Response
from rest_framework_blueprint.structures import Field, Structure
from rest_framework_blueprint.types import get_mson_type, TYPE_ENUM


register = template.Library()


INDENT = '    '


def indent_text(text, indent):
    return '\n'.join([INDENT * indent + line for line in text.split('\n')])


@register.simple_tag
def resource(instance, indent=0):
    if not instance:
        return ''

    if not isinstance(instance, Resource):
        raise TypeError('The argument is not instance of Action')

    markdown = render_to_string('rest_framework_blueprint/resource.md', {'resource': instance})
    return indent_text(markdown, indent=indent)


@register.simple_tag
def action(instance, indent=0):
    if not instance:
        return ''

    if not isinstance(instance, Action):
        raise TypeError('The argument is not instance of Action')

    parameters = Structure.merge(instance.resource.parameters, instance.parameters)

    context = {
        'action': instance,
        'method': instance.method,
        'document': instance.document,
        'parameters': parameters,
        'requests': instance.requests,
        'responses': instance.responses,
    }

    markdown = render_to_string('rest_framework_blueprint/action.md', context)
    return indent_text(markdown, indent=indent)


@register.simple_tag
def request(instance, indent=0):
    if not instance:
        return ''

    if not isinstance(instance, Request):
        raise TypeError('The argument is not instance of Request')

    context = {
        'request': instance,
        'action': instance.action,
        'media_type': instance.media_type,
        'headers': instance.headers,
        'attribute': instance.attribute,
        'body': instance.body,
    }

    markdown = render_to_string('rest_framework_blueprint/request.md', context)
    return indent_text(markdown, indent=indent)


@register.simple_tag
def response(instance, indent=0):
    if not instance:
        return ''

    if not isinstance(instance, Response):
        raise TypeError('The argument is not instance of Response')

    context = {
        'response': instance,
        'action': instance.action,
        'media_type': instance.media_type,
        'headers': instance.headers,
        'attribute': instance.attribute,
        'body': instance.body,
        'status': instance.status,
    }

    markdown = render_to_string('rest_framework_blueprint/response.md', context)
    return indent_text(markdown, indent=indent)


@register.simple_tag
def parameters(instance, indent=0):
    if not instance:
        return ''

    if not isinstance(instance, Structure):
        raise TypeError('The argument is not instance of Structure')

    context = {
        'parameters': instance,
        'fields': instance.fields,
    }

    markdown = render_to_string('rest_framework_blueprint/parameters.md', context)
    return indent_text(markdown, indent=indent)


@register.simple_tag
def attribute(instance, indent=1):
    if not instance:
        return ''

    if not isinstance(instance, Structure):
        raise TypeError('The argument is not instance of Structure')

    context = {
        'attribute': instance,
        'fields': instance.fields,
    }

    markdown = render_to_string('rest_framework_blueprint/attributes.md', context)
    return indent_text(markdown, indent=indent)


@register.simple_tag
def field(instance, indent=1):
    if not instance:
        return ''

    if not isinstance(instance, Field):
        raise TypeError('The argument is not instance of Field')

    context = {
        'field': instance,
        'name': instance.name,
        'type': instance.type,
        'choices': instance.choices,
        'label': instance.label,
        'required': instance.required,
        'default': instance.default,
        'help_text': instance.help_text,
    }

    markdown = render_to_string('rest_framework_blueprint/field.md', context)
    return indent_text(markdown, indent=indent)


@register.filter(name='type')
def get_type(field):
    if not isinstance(field, Field):
        raise TypeError('The argument is not instance of Field')

    mson_type = get_mson_type(field.type)
    if field.choices:
        mson_type = '{}[{}]'.format(TYPE_ENUM, mson_type)

    return mson_type


@register.filter(name='path')
def get_path(instance):
    if isinstance(instance, Resource):
        return instance.path

    if not isinstance(instance, Action):
        raise TypeError('The argument is not instance of Resource or Action')

    if not instance.parameters:
        return instance.resource.path

    return instance.resource.path + '{{?{}}}'.format(','.join([
        field.name
        for field in instance.parameters.fields
    ]))
