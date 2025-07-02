from typing import Any, Dict
from wagtail.api.v2.serializers import PageSerializer
from rest_framework import serializers


class CustomPageSerializer(PageSerializer):
    
    def get_tags(self, instance):
        try:
            # まずtagsフィールドを試す
            if hasattr(instance, 'tags') and instance.tags:
                return [tag.name for tag in instance.tags.all()]
            # tagged_itemsから取得を試す
            elif hasattr(instance, 'tagged_items'):
                return [item.tag.name for item in instance.tagged_items.all()]
        except (AttributeError, Exception):
            pass
        return []
    
    def to_representation(self, instance):
        page_data = super().to_representation(instance)
        
        # meta.html_url を削除
        if 'meta' in page_data and 'html_url' in page_data['meta']:
            page_data['meta'].pop('html_url', None)
        
        # last_published_atを追加
        if hasattr(instance, 'last_published_at') and instance.last_published_at:
            page_data['meta']['last_published_at'] = instance.last_published_at
        
        # tagsを追加
        page_data['tags'] = self.get_tags(instance)
        
        return page_data
    
    
class BlogStreamFieldRichtextPageSerializer(CustomPageSerializer):
    pass


class BlogStreamFieldMarkdownPageSerializer(CustomPageSerializer):
    pass


class TagSerializer(serializers.ModelSerializer):
    pass