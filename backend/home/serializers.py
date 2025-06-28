from typing import Any, Dict
from wagtail.api.v2.serializers import PageSerializer
from rest_framework import serializers


class CustomPageSerializer(PageSerializer):
    
    def to_representation(self, instance):
        page_data = super().to_representation(instance)
        
        # meta.html_url を削除
        if 'meta' in page_data and 'html_url' in page_data['meta']:
            page_data['meta'].pop('html_url', None)
        
        # last_published_atを追加
        if hasattr(instance, 'last_published_at') and instance.last_published_at:
            page_data['meta']['last_published_at'] = instance.last_published_at
        
        return page_data
    
    
class BlogStreamFieldRichtextPageSerializer(CustomPageSerializer):
    pass


class BlogStreamFieldMarkdownPageSerializer(CustomPageSerializer):
    pass


class TagSerializer(serializers.ModelSerializer):
    pass