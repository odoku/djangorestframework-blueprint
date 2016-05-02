# -*- coding: utf-8 -*-

from rest_framework.filters import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .serializers import ArticleSerializer
from .filters import ArticleFilter


class IndexView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticleFilter


class DetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
