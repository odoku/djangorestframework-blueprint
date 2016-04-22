# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import DetailView, IndexView


urlpatterns = [
    url(r'^article$', IndexView.as_view(), name='index'),
    url(r'^article/(?P<pk>\d+)$', DetailView.as_view(), name='detail'),
]
