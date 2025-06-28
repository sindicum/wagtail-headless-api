import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('home')


class RequestLoggingMiddleware(MiddlewareMixin):
    """リクエスト/レスポンスのログを記録するミドルウェア"""
    
    def process_request(self, request):
        # リクエスト開始時刻を記録
        request._start_time = time.time()
        
        # リクエスト情報をログ
        logger.info(
            f"Request: {request.method} {request.path} "
            f"from {self.get_client_ip(request)}"
        )
        
        # POSTデータのログ（センシティブな情報は除外）
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                body = json.loads(request.body)
                # パスワードなどのセンシティブな情報を除外
                safe_body = {k: v for k, v in body.items() 
                            if 'password' not in k.lower() and 'token' not in k.lower()}
                logger.debug(f"POST data: {safe_body}")
            except:
                pass
    
    def process_response(self, request, response):
        # レスポンス時間を計算
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            logger.info(
                f"Response: {response.status_code} for {request.path} "
                f"in {duration:.3f}s"
            )
        
        return response
    
    def process_exception(self, request, exception):
        # エラー情報をログ
        logger.error(
            f"Exception: {exception.__class__.__name__} for {request.path}",
            exc_info=True
        )
    
    def get_client_ip(self, request):
        """クライアントIPアドレスを取得"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip