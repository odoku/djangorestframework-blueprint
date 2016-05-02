# -*- coding: utf-8 -*-

import pytest

from django.views.generic import View
from rest_framework import status
from rest_framework_blueprint.utils import (
    get_accept_media_types,
    get_allowed_methods,
    get_filter_class,
    get_filter_fields,
    get_response_status,
    get_serializer_class,
    get_serializer_fields,
    get_urlpatterns,
    get_views,
    is_api_view,
)

from testapp.articles.views import IndexView
from testapp.articles.serializers import ArticleSerializer
from testapp.articles.filters import ArticleFilter


@pytest.mark.django_db
class TestGetURLPatterns(object):
    def test_success(self):
        urlpatterns = get_urlpatterns()
        assert urlpatterns


@pytest.mark.django_db
class TestGetViews(object):
    def test_success(self):
        views = get_views(get_urlpatterns())
        assert views


@pytest.mark.django_db
class TestIsAPIView(object):
    def test_success(self):
        assert is_api_view(IndexView.as_view())
        assert not is_api_view(View.as_view())


@pytest.mark.django_db
class TestGetSerializerClass(object):
    def test_success(self):
        serializer_class = get_serializer_class(IndexView)
        assert serializer_class
        assert serializer_class == ArticleSerializer


@pytest.mark.django_db
class TestGetSerializerFields(object):
    def test_success(self):
        fields = get_serializer_fields(ArticleSerializer)
        assert fields
        assert len(fields) == 4


@pytest.mark.django_db
class TestGetFilterClass(object):
    def test_success(self):
        filter_class = get_filter_class(IndexView)
        assert filter_class
        assert filter_class == ArticleFilter


@pytest.mark.django_db
class TestGetFilterFields(object):
    def test_success(self):
        fields = get_filter_fields(ArticleFilter)
        assert fields
        assert len(fields) == 3


@pytest.mark.django_db
class TestGetAllowedMethods(object):
    def test_success(self):
        methods = get_allowed_methods(IndexView)
        assert methods
        assert len(methods) == 2
        assert 'GET' in methods
        assert 'POST' in methods


@pytest.mark.django_db
class TestGetAcceptMediaTypes(object):
    def test_success(self):
        types = get_accept_media_types(IndexView)
        assert types
        assert len(types) == 3
        assert 'application/json' in types
        assert 'application/x-www-form-urlencoded' in types
        assert 'multipart/form-data' in types


@pytest.mark.django_db
class TestGetResponseStatus(object):
    @pytest.mark.parametrize(
        'view_class, method, status_code',
        [
            (IndexView, 'GET', status.HTTP_200_OK),
            (IndexView, 'POST', status.HTTP_201_CREATED),
        ],
    )
    def test_success(self, view_class, method, status_code):
        result = get_response_status(method, view_class)
        assert result
        assert result == status_code
