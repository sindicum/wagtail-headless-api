from django.db import models
from django.utils import timezone

from wagtail.models import Page
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.blocks import CharBlock, RichTextBlock, TextBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtailcodeblock.blocks import CodeBlock


def stream_field_markdown_body():
    body = StreamField([
        ('chapter', CharBlock(label="chapter")),
        ('section', CharBlock(label="section")),
        ('markdown', TextBlock(label="markdown")),
        ('code', CodeBlock(label="Code Snippet", default_language='python')),
        ('image', ListBlock(ImageChooserBlock(label="image"))),
    ], blank=True, use_json_field=True)
    return body

def stream_field_richtext_body():
    body = StreamField([
        ('chapter', CharBlock(label="chapter")),
        ('section', CharBlock(label="section")),
        ('contents', RichTextBlock(label="contents")),
        ('code', CodeBlock(label="Code Snippet", default_language='python')),
        ('image', ListBlock(ImageChooserBlock(label="image"))),
    ], blank=True, use_json_field=True)
    return body


class BlogRootPage(Page):
    # ページの親子関係
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ['home.BlogStreamFieldRichtextPage','home.BlogStreamFieldMarkdownPage']   

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey( 
        Page,  # 複数のPageで共通利用するためPageに紐づけ
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )

class BlogStreamFieldRichtextPage(Page):
    parent_page_types = ['home.BlogRootPage']
    
    published_date = models.DateField("Published date", default=timezone.now)
    updated_at = models.DateField("Updated at", auto_now=True)
    body = stream_field_richtext_body()
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('published_date', heading="投稿日"),
        FieldPanel('body', heading="内容"),
        FieldPanel('tags', heading="ハッシュタグ"),
    ]

    # API表示フィールド
    api_fields = [
        APIField('title'),
        APIField('published_date'),
        APIField('updated_at'),
        APIField('body'),
        APIField('tags'),
    ]


class BlogStreamFieldMarkdownPage(Page):
    # ページの親子関係
    parent_page_types = ['home.BlogRootPage']
    
    published_date = models.DateField("Published date", default=timezone.now)
    updated_at = models.DateField("Updated at", auto_now=True)
    body = stream_field_markdown_body()
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('published_date', heading="投稿日"),
        FieldPanel('body', heading="内容"),
        FieldPanel('tags', heading="ハッシュタグ"),
    ]

    # API表示フィールド
    api_fields = [
        APIField('title'),
        APIField('published_date'),
        APIField('updated_at'),
        APIField('body', serializer=None),  # StreamFieldの内容をそのまま表示
        APIField('tags'),
    ]
