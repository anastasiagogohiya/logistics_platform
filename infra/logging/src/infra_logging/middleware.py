# infra/logging/src/infra_logging/middleware.py
import logging
import time
import uuid

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestIdMiddleware(MiddlewareMixin):
    """Middleware для добавления request_id к запросам"""

    def process_request(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = request_id
        request.META["REQUEST_ID"] = request_id

    def process_response(self, request, response):
        if hasattr(request, "request_id"):
            response["X-Request-ID"] = request.request_id
        return response


class LoggingMiddleware:
    """Middleware для логирования запросов"""

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        start_time = time.time()
        request_id = getattr(request, "request_id", None)

        # Логируем с request_id через extra
        self.logger.info(
            f"Incoming: {request.method} {request.path}",
            extra={"request_id": request_id} if request_id else {},
        )

        response = self.get_response(request)

        duration = time.time() - start_time
        self.logger.info(
            f"Completed: {request.method} {request.path} - {response.status_code} - {duration:.3f}s",
            extra={"request_id": request_id} if request_id else {},
        )

        return response


class FastAPIRequestIdMiddleware:
    """Middleware для FastAPI"""

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        scope["request_id"] = request_id

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                headers[b"x-request-id"] = request_id.encode()
                message["headers"] = list(headers.items())
            await send(message)

        self.logger.info(f"FastAPI Request: {request_id}", extra={"request_id": request_id})

        await self.app(scope, receive, send_wrapper)
