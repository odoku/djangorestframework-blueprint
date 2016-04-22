# -*- coding: utf-8 -*-

from django.db import models


class Team(models.Model):
    name = models.CharField('name', max_length=50)


class Author(models.Model):
    team = models.ForeignKey(Team)
    name = models.CharField('name', max_length=50)


class Article(models.Model):
    author = models.ForeignKey(
        Author,
        verbose_name='author',
        related_name='articles',
    )
    title = models.CharField('title', max_length=50)
    body = models.TextField('body')

    class Meta:
        unique_together = (('author', 'title'),)
