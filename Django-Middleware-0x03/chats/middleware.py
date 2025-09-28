import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # Called once when Django starts
        self.get_response = get_response
        # Set up a dedicated logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        # Called on every request
        user = request.user if request.user.is_authenticated else "Anonymous"
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)
