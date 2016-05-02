# -*- coding: utf-8 -*-

from django.forms.widgets import TextInput
import django_filters
from rest_framework.filters import FilterSet

from .models import Article, Author, Team


class TeamFilter(FilterSet):
    class Meta:
        model = Team
        fields = ('name',)


class AuthorFilter(FilterSet):
    class Meta:
        model = Author
        fields = ('team', 'name',)


class ArticleFilter(FilterSet):
    title = django_filters.CharFilter(
        name='title',
        label='Name',
        lookup_expr='startswith',
        help_text='Case-sensitive starts-with.',
        widget=TextInput(),
    )

    body = django_filters.CharFilter(
        name='body',
        label='Body',
        lookup_expr='icontains',
        help_text='Case-insensitive containment test.',
        widget=TextInput(),
    )

    class Meta:
        model = Article
        fields = ('author', 'title', 'body')
