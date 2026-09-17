"""A minimal, dependency-free rate limiter for the public form endpoints
(Contact, Hire Me). It is intentionally simple — for real production
traffic behind Render/Hostinger, prefer django-ratelimit or an
edge/WAF-level limit, but this stops the most naive spam bots without
adding infrastructure.
"""
import time
from collections import defaultdict

from django.http import HttpResponseForbidden

RATE_LIMITED_PATHS = {"/contact/", "/hire/"}
WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 5

_hits = defaultdict(list)


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path in RATE_LIMITED_PATHS:
            ip = self._client_ip(request)
            now = time.time()
            key = (ip, request.path)
            recent = [t for t in _hits[key] if now - t < WINDOW_SECONDS]
            if len(recent) >= MAX_REQUESTS_PER_WINDOW:
                return HttpResponseForbidden("Too many submissions. Please try again in a minute.")
            recent.append(now)
            _hits[key] = recent
        return self.get_response(request)

    @staticmethod
    def _client_ip(request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")
