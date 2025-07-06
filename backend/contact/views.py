from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
import json
import ipaddress
import logging
from .serializers import ContactSerializer

# ロガーの設定
logger = logging.getLogger('contact')
security_logger = logging.getLogger('django.security')


def get_client_ip(request):
    """信頼できるプロキシを考慮してクライアントIPを取得"""
    # 信頼できるプロキシのリスト（設定から取得、デフォルトは空）
    trusted_proxies = getattr(settings, 'TRUSTED_PROXIES', [])
    
    # まず直接接続のIPを取得
    remote_addr = request.META.get('REMOTE_ADDR')
    
    # X-Forwarded-Forヘッダーがある場合
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for and remote_addr in trusted_proxies:
        # 信頼できるプロキシからのリクエストの場合のみX-Forwarded-Forを使用
        # 最初のIPアドレスを取得（複数のプロキシを経由している場合）
        ip = x_forwarded_for.split(',')[0].strip()
        
        # IPアドレスの妥当性を検証
        try:
            ipaddress.ip_address(ip)
            logger.debug(f"IPアドレス取得: {ip} (X-Forwarded-For使用)")
            return ip
        except ValueError:
            # 無効なIPアドレスの場合は直接接続のIPを使用
            logger.warning(f"無効なX-Forwarded-For: {x_forwarded_for}, REMOTE_ADDRを使用: {remote_addr}")
            return remote_addr
    
    logger.debug(f"IPアドレス取得: {remote_addr} (REMOTE_ADDR使用)")
    return remote_addr


def check_rate_limit(ip):
    """レート制限のチェック（設定から値を取得）"""
    # 設定から制限値を取得（デフォルト値付き）
    minute_limit = getattr(settings, 'CONTACT_RATE_LIMIT_MINUTE', 3)
    hour_limit = getattr(settings, 'CONTACT_RATE_LIMIT_HOUR', 10)
    minute_timeout = getattr(settings, 'CONTACT_RATE_LIMIT_MINUTE_TIMEOUT', 60)
    hour_timeout = getattr(settings, 'CONTACT_RATE_LIMIT_HOUR_TIMEOUT', 3600)
    
    minute_key = f"contact_rate_limit_minute_{ip}"
    hour_key = f"contact_rate_limit_hour_{ip}"
    
    minute_count = cache.get(minute_key, 0)
    hour_count = cache.get(hour_key, 0)
    
    if minute_count >= minute_limit:
        security_logger.warning(
            f"レート制限超過 (分): IP={ip}, 回数={minute_count}/{minute_limit}"
        )
        return False, "送信回数の上限に達しました。しばらく経ってから再度お試しください。"
    
    if hour_count >= hour_limit:
        security_logger.warning(
            f"レート制限超過 (時間): IP={ip}, 回数={hour_count}/{hour_limit}"
        )
        return False, "送信回数の上限に達しました。しばらく経ってから再度お試しください。"
    
    cache.set(minute_key, minute_count + 1, minute_timeout)
    cache.set(hour_key, hour_count + 1, hour_timeout)
    
    logger.debug(f"レート制限チェック通過: IP={ip}, 分={minute_count+1}/{minute_limit}, 時間={hour_count+1}/{hour_limit}")
    return True, None


@api_view(['POST'])
@permission_classes([AllowAny])
def contact_create(request):
    client_ip = get_client_ip(request)
    logger.info(f"問い合わせAPIアクセス: IP={client_ip}")
    
    rate_limit_ok, rate_limit_message = check_rate_limit(client_ip)
    if not rate_limit_ok:
        return Response({
            'success': False,
            'message': rate_limit_message
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    try:
        if request.content_type != 'application/json':
            security_logger.warning(f"不正なContent-Type: {request.content_type}, IP={client_ip}")
            return Response({
                'success': False,
                'errors': {'detail': ['Content-Type must be application/json']}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ContactSerializer(data=request.data)
        
        if serializer.is_valid():
            contact = serializer.save()
            logger.info(
                f"問い合わせ受信: ID={contact.id}, 名前={contact.name}, "
                f"メール={contact.email}, IP={client_ip}"
            )
            return Response({
                'success': True,
                'message': 'お問い合わせを受け付けました。'
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(
                f"バリデーションエラー: {serializer.errors}, IP={client_ip}"
            )
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except json.JSONDecodeError as e:
        security_logger.error(f"JSONパースエラー: {str(e)}, IP={client_ip}")
        return Response({
            'success': False,
            'errors': {'detail': ['Invalid JSON format']}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(
            f"問い合わせAPIエラー: {e.__class__.__name__}: {str(e)}, IP={client_ip}",
            exc_info=True
        )
        return Response({
            'success': False,
            'message': 'サーバーエラーが発生しました。'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
