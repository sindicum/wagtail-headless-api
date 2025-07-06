from rest_framework import serializers
from django.utils.html import strip_tags
from django.core.validators import EmailValidator
from django.utils.text import slugify
import re
import bleach
import logging
from .models import Contact

# ロガーの設定
logger = logging.getLogger('contact')
security_logger = logging.getLogger('django.security')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("名前は必須項目です。")
        
        # HTMLタグとスクリプトを除去
        cleaned_value = bleach.clean(value, tags=[], strip=True).strip()
        
        if not cleaned_value:
            raise serializers.ValidationError("名前は必須項目です。")
        
        if len(cleaned_value) > 100:
            raise serializers.ValidationError("名前は100文字以内で入力してください。")
        
        # 不正な文字パターンのチェック
        if re.search(r'[<>"\']', cleaned_value):
            security_logger.warning(
                f"名前フィールドに特殊文字を検出: {value[:50]}..."
            )
            raise serializers.ValidationError("特殊文字は使用できません。")
        
        return cleaned_value
    
    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("メールアドレスは必須項目です。")
        
        # HTMLタグを除去
        cleaned_value = bleach.clean(value, tags=[], strip=True).strip().lower()
        
        if not cleaned_value:
            raise serializers.ValidationError("メールアドレスは必須項目です。")
        
        # Djangoのメールバリデータを使用
        email_validator = EmailValidator(message="正しいメールアドレスを入力してください。")
        try:
            email_validator(cleaned_value)
        except serializers.ValidationError:
            raise serializers.ValidationError("正しいメールアドレスを入力してください。")
        
        if len(cleaned_value) > 100:
            raise serializers.ValidationError("メールアドレスは100文字以内で入力してください。")
        
        return cleaned_value
    
    def validate_message(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("メッセージは必須項目です。")
        
        # HTMLタグとスクリプトを除去（改行は保持）
        cleaned_value = bleach.clean(
            value,
            tags=[],
            strip=True,
            strip_comments=True
        ).strip()
        
        if not cleaned_value:
            raise serializers.ValidationError("メッセージは必須項目です。")
        
        if len(cleaned_value) > 1000:
            raise serializers.ValidationError("メッセージは1000文字以内で入力してください。")
        
        # SQLインジェクションパターンのチェック
        sql_patterns = [r'(union|select|insert|update|delete|drop|create)\s', r'--', r'/\*', r'\*/']  
        for pattern in sql_patterns:
            if re.search(pattern, cleaned_value, re.IGNORECASE):
                security_logger.warning(
                    f"SQLインジェクションパターンを検出: パターン={pattern}, "
                    f"メッセージ={cleaned_value[:100]}..."
                )
                raise serializers.ValidationError("不正な文字列が含まれています。")
        
        logger.debug(f"メッセージバリデーション成功: 長さ={len(cleaned_value)}文字")
        return cleaned_value