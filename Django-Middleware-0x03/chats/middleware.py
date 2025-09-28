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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Deny access to the chat between 6 PM (18:00) and 9 PM (21:00)
        or outside the allowed window depending on interpretation.
        """
        current_hour = datetime.now().hour
        # Block if time is outside 6:00 to 21:00 (i.e., not between 6 AM and 9 PM)
        if current_hour < 6 or current_hour > 21:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Chat is accessible only between 6 AM and 9 PM.</p>"
            )

        return self.get_response(request)
        

