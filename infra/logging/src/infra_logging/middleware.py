import uuid
import logging


# ===== ДЛЯ DJANGO (синхронный) =====
class RequestIdMiddleware:
    """Middleware для Django"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get('X-Request-Id', str(uuid.uuid4()))
        request.request_id = request_id

        logger = logging.getLogger()
        old_factory = logger.getChild

        def adapter_factory(name):
            return logging.LoggerAdapter(logging.getLogger(name), {'request_id': request_id})

        logger.getChild = adapter_factory

        response = self.get_response(request)
        response['X-Request-Id'] = request_id
        return response


# ===== ДЛЯ FASTAPI (асинхронный) =====
# ✅ Импорт ТОЛЬКО когда нужен FastAPI
try:
    from starlette.middleware.base import BaseHTTPMiddleware


    class FastAPIRequestIdMiddleware(BaseHTTPMiddleware):
        """Middleware для FastAPI"""

        async def dispatch(self, request, call_next):
            request_id = request.headers.get('X-Request-Id', str(uuid.uuid4()))
            request.state.request_id = request_id

            logger = logging.getLogger()
            logger = logging.LoggerAdapter(logger, {'request_id': request_id})

            response = await call_next(request)
            response.headers['X-Request-Id'] = request_id
            return response

except ImportError:
    # Если starlette не установлен (Django проект), просто пропускаем
    pass