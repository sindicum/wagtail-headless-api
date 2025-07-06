from django.db import models
from django.contrib.auth.models import User
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class Contact(ClusterableModel):
    STATUS_CHOICES = [
        ('new', '未対応'),
        ('in_progress', '対応中'),
        ('completed', '対応済み'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='名前')
    email = models.EmailField(max_length=100, verbose_name='メールアドレス')
    message = models.TextField(max_length=1000, verbose_name='メッセージ')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name='ステータス'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        verbose_name = '問い合わせ'
        verbose_name_plural = '問い合わせ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    def get_reply_count(self):
        return self.replies.count()
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name', read_only=True),
            FieldPanel('email', read_only=True),
            FieldPanel('message', read_only=True),
        ], heading='問い合わせ内容'),
        MultiFieldPanel([
            FieldPanel('status'),
        ], heading='管理情報'),
        InlinePanel('replies', label='返信履歴'),
    ]


class ContactReply(models.Model):
    contact = ParentalKey(
        Contact, 
        on_delete=models.CASCADE, 
        related_name='replies',
        verbose_name='問い合わせ'
    )
    subject = models.CharField(max_length=200, verbose_name='件名')
    body = models.TextField(verbose_name='返信内容')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='送信日時')
    sent_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='送信者'
    )
    
    class Meta:
        verbose_name = '返信'
        verbose_name_plural = '返信'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.contact.name}への返信 - {self.subject}"
    
    panels = [
        FieldPanel('subject'),
        FieldPanel('body'),
    ]


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, verbose_name='テンプレート名')
    subject = models.CharField(max_length=200, verbose_name='件名')
    body = models.TextField(verbose_name='本文')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        verbose_name = 'メールテンプレート'
        verbose_name_plural = 'メールテンプレート'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    panels = [
        FieldPanel('name'),
        FieldPanel('subject'),
        FieldPanel('body'),
    ]
