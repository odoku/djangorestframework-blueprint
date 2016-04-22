# -*- coding: utf-8 -*-

import factory
from factory.fuzzy import FuzzyText

from .models import Author, Article, Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'team_{0}'.format(n))


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'author_{0}'.format(n))


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
        django_get_or_create = ('author', 'title',)

    title = factory.Sequence(lambda n: 'title_{0}'.format(n))
    body = FuzzyText(length=2000)
