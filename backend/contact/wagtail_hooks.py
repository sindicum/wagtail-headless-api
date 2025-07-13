import logging
from django.urls import path
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from wagtail import hooks
from wagtail.snippets.views.snippets import SnippetViewSet, EditView as SnippetEditView
from wagtail.snippets.models import register_snippet
from .models import Contact, ContactReply, EmailTemplate
from .forms import ContactEditForm

logger = logging.getLogger(__name__)


class ContactEditView(SnippetEditView):
    form_class = ContactEditForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_templates'] = EmailTemplate.objects.all()
        return context


class ContactViewSet(SnippetViewSet):
    model = Contact
    menu_label = '問い合わせ管理'
    menu_icon = 'mail'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['name', 'email', 'get_status_display', 'created_at', 'get_reply_count']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    ordering = ['-created_at']
    edit_view_class = ContactEditView
    


class EmailTemplateViewSet(SnippetViewSet):
    model = EmailTemplate
    menu_label = 'メールテンプレート'
    menu_icon = 'doc-full'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['name', 'subject', 'created_at']
    search_fields = ['name', 'subject', 'body']
    ordering = ['name']


register_snippet(Contact, viewset=ContactViewSet)
register_snippet(EmailTemplate, viewset=EmailTemplateViewSet)


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return """
    <style>
    .status-tag {
        padding: 2px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        color: white;
    }
    .status-tag.serious {
        background-color: #cd3238;
    }
    .status-tag.warning {
        background-color: #f39c12;
    }
    .status-tag.success {
        background-color: #189370;
    }
    </style>
    """


def send_reply_email(request, contact_id):
    """メール返信を送信するビュー"""
    contact = get_object_or_404(Contact, id=contact_id)
    logger.info(f"メール返信ページアクセス: 問い合わせID={contact_id}, ユーザー={request.user.username}")
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        
        if subject and body:
            try:
                # 返信レコードを作成
                reply = ContactReply.objects.create(
                    contact=contact,
                    subject=subject,
                    body=body,
                    sent_by=request.user
                )
                
                # メール送信
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact.email],
                    fail_silently=False,
                )
                
                # ステータスを対応中に更新
                if contact.status == 'new':
                    contact.status = 'in_progress'
                    contact.save()
                
                logger.info(
                    f"メール返信成功: 問い合わせID={contact_id}, 宛先={contact.email}, "
                    f"件名={subject[:50]}..., ユーザー={request.user.username}"
                )
                messages.success(request, f'{contact.name}にメールを送信しました。')
                return redirect('wagtailsnippets_contact_contact:edit', contact.id)
                
            except Exception as e:
                logger.error(
                    f"メール送信エラー: 問い合わせID={contact_id}, エラー={str(e)}, "
                    f"ユーザー={request.user.username}",
                    exc_info=True
                )
                messages.error(request, f'メール送信に失敗しました: {str(e)}')
        else:
            messages.error(request, '件名と本文を入力してください。')
    
    return redirect('wagtailsnippets_contact_contact:edit', contact.id)


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('contact/send-reply/<int:contact_id>/', send_reply_email, name='contact_send_reply'),
    ]