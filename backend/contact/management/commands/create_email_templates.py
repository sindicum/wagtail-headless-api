from django.core.management.base import BaseCommand
from contact.models import EmailTemplate


class Command(BaseCommand):
    help = 'Create sample email templates'

    def handle(self, *args, **options):
        templates = [
            {
                'name': '初回返信テンプレート',
                'subject': 'お問い合わせありがとうございます',
                'body': '''{{name}}様

この度は、お問い合わせいただきありがとうございます。

いただいたお問い合わせ内容を確認させていただき、
担当者より回答させていただきます。

今後ともよろしくお願いいたします。

担当者名: {{担当者名}}
'''
            },
            {
                'name': '完了通知テンプレート',
                'subject': 'お問い合わせ対応完了のお知らせ',
                'body': '''{{name}}様

お問い合わせいただいた件につきまして、
対応が完了いたしましたのでご連絡いたします。

ご不明な点がございましたら、
お気軽にお問い合わせください。

今後ともよろしくお願いいたします。

担当者名: {{担当者名}}
'''
            },
            {
                'name': '詳細確認テンプレート',
                'subject': 'お問い合わせ内容の詳細確認について',
                'body': '''{{name}}様

お問い合わせいただき、ありがとうございます。

より詳しく対応させていただくため、
以下について教えていただけますでしょうか。

- 
- 
- 

お手数をおかけいたしますが、
よろしくお願いいたします。

担当者名: {{担当者名}}
'''
            }
        ]

        for template_data in templates:
            template, created = EmailTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'subject': template_data['subject'],
                    'body': template_data['body']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Template already exists: {template.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Email templates creation completed!')
        )