# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='djangorestframework-blueprint',
    version='0.0.1',
    description='Export APIBlueprint for Django REST Framework.',
    author='odoku',
    author_email='masashi.onogawa@wamw.jp',
    keywords='django,api,rest,apiblueprint',
    url='http://github.com/odoku/djangorestframework-blueprint',

    packages=[
        'rest_framework_blueprint',
        'rest_framework_blueprint.management',
        'rest_framework_blueprint.templates',
        'rest_framework_blueprint.templatetags',
    ],
    install_requires=[
        'Django>=1.9.5',
        'django-filter>=0.13.0',
        'djangorestframework>=3.3.3',
    ],
    extras_require={
        'test': ['pytest==2.9.1'],
    }
)
