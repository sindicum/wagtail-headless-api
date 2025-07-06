from wagtail.admin.forms import WagtailAdminModelForm
from django import forms
from .models import Contact


class ContactEditForm(WagtailAdminModelForm):
    """Contact編集用のカスタムフォーム（送信内容を読み取り専用にする）"""
    
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly', 'disabled': 'disabled'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'disabled': 'disabled'}),
            'message': forms.Textarea(attrs={'readonly': 'readonly', 'disabled': 'disabled', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 送信されてきた内容のフィールドを無効化
        if self.instance and self.instance.pk:
            self.fields['name'].disabled = True
            self.fields['email'].disabled = True
            self.fields['message'].disabled = True