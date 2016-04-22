# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import codecs
import sys

from django.core.management.base import BaseCommand

from rest_framework_blueprint.factories import create_document_from_urlpatterns
from rest_framework_blueprint.utils import get_urlpatterns
from rest_framework_blueprint.builders import blueprint


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '-b', '--base_url', dest='base_url',
            action='store', default='http://localhost:8000',
        )
        parser.add_argument(
            '-t', '--title', dest='title',
            action='store', default='API Documentation',
        )
        parser.add_argument(
            '-d', '--description', dest='description',
            action='store', default='',
        )
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        urlpatterns = get_urlpatterns()
        document = create_document_from_urlpatterns(
            urlpatterns,
            base_url=options['base_url'],
            title=options['title'],
            description=options['description'],
        )
        print(blueprint(document), file=sys.stdout)
