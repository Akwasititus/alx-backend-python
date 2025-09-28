import logging
from datetime import 
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

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


class OffensiveLanguageMiddleware:
    """
    Limits each IP to 5 POST requests (chat messages) per minute.
    """

    # Shared across requests – keeps timestamps of recent messages per IP
    _ip_activity = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track POST requests to the chat app (message sends)
        if request.method == "POST" and request.path.startswith("/chats"):
            ip = self._get_ip(request)
            now = datetime.now()

            # Purge timestamps older than 1 minute for this IP
            window_start = now - timedelta(minutes=1)
            timestamps = self._ip_activity.get(ip, [])
            timestamps = [t for t in timestamps if t > window_start]

            # Check limit
            if len(timestamps) >= 5:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1>"
                    "<p>You have exceeded the limit of 5 messages per minute.</p>"
                )

            # Record this message timestamp
            timestamps.append(now)
            self._ip_activity[ip] = timestamps

        return self.get_response(request)

    def _get_ip(self, request):
        """
        Safely extract client IP address.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")


class RolePermissionMiddleware:
    """
    Blocks access to certain views unless the user is an admin or moderator.
    Assumes request.user has an attribute or group that defines their role.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # You can customize which paths need admin/moderator protection
        protected_paths = ["/chats/admin/", "/chats/manage/"]

        if any(request.path.startswith(p) for p in protected_paths):
            user = getattr(request, "user", None)

            # Ensure the user is authenticated and has the correct role/group
            if not (user and user.is_authenticated and
                    (getattr(user, "is_superuser", False) or
                     user.groups.filter(name__in=["admin", "moderator"]).exists())):
                return HttpResponseForbidden("403 Forbidden: Insufficient role permissions.")

        return self.get_response(request)


        






