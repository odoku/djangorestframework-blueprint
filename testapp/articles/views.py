# -*- coding: utf-8 -*-

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .serializers import ArticleSerializer


class IndexView(ListCreateAPIView):
    serializer_class = ArticleSerializer


class DetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
