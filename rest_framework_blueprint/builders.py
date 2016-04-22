# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.template.loader import render_to_string


BLUEPRINT_TEMPLATE_NAME = 'rest_framework_blueprint/blueprint.md'


def blueprint(document):
    markdown = render_to_string(BLUEPRINT_TEMPLATE_NAME, {'document': document})

    lines = []
    for line in markdown.split('\n'):
        if line.strip() == '':
            continue

        if line.startswith('#'):
            line = '\n\n' + line + '\n'

        if line.startswith('+'):
            line = '\n' + line

        lines.append(line)
    markdown = '\n'.join(lines)

    return markdown
