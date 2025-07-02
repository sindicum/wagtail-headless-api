from django.conf import settings
from wagtail.api.v2.views import BaseAPIViewSet, PagesAPIViewSet
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from taggit.models import Tag

from .models import BlogStreamFieldRichtextPage, BlogStreamFieldMarkdownPage
from .serializers import BlogStreamFieldRichtextPageSerializer, BlogStreamFieldMarkdownPageSerializer, CustomPageSerializer,TagSerializer


class CustomPagesAPIViewSet(PagesAPIViewSet):
    """BlogRootPageを除外したPagesAPIViewSet"""
    base_serializer_class = CustomPageSerializer
    
    # レンダラーを環境に応じて設定
    if settings.DEBUG:
        renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    else:
        renderer_classes = [JSONRenderer]
    
    # known_query_parametersにtagを追加
    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(['tag'])

    @classmethod
    def get_available_fields(cls, model, db_fields_only=False):
        fields = super().get_available_fields(model, db_fields_only)
        # カスタムフィールド 'last_published_at' を追加
        if hasattr(model, 'last_published_at'):
            fields.append('last_published_at')
        return fields
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # BlogRootPageを除外
        queryset = queryset.exclude(
            content_type__model='blogrootpage'
        )
        
        # タグ情報をプリフェッチ
        queryset = queryset.prefetch_related('tagged_items__tag')
        
        # タグフィルタリング
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tagged_items__tag__name__iexact=tag).distinct()
        
        # 並び順を指定（デフォルトは降順）
        order = self.request.GET.get('order', '-last_published_at')
        if order in ['last_published_at', '-last_published_at']:
            queryset = queryset.order_by(order)
        
        return queryset



class BlogStreamFieldRichtextPagesAPIViewSet(PagesAPIViewSet):
    base_serializer_class = BlogStreamFieldRichtextPageSerializer
    model = BlogStreamFieldRichtextPage


class BlogStreamFieldMarkdownPagesAPIViewSet(PagesAPIViewSet):
    base_serializer_class = BlogStreamFieldMarkdownPageSerializer
    model = BlogStreamFieldMarkdownPage


class TagsAPIViewSet(BaseAPIViewSet):
    base_serializer_class = TagSerializer
    model = Tag
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    
    # レンダラーを環境に応じて設定
    if settings.DEBUG:
        renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    else:
        renderer_classes = [JSONRenderer]

    known_query_parameters = BaseAPIViewSet.known_query_parameters.union([
        'fields',
        'order',
        'search',
    ])
    body_fields = [
        'id',
        'name',
        'slug',
    ]
    listing_default_fields = body_fields
