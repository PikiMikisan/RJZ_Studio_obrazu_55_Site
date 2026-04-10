from django.http import HttpResponse


class RenderHealthcheckMiddleware:
    """Short-circuit Render probes before Django validates the Host header."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        if request.path_info == "/healthz/" and request.method in {"GET", "HEAD"}:
            return HttpResponse("ok", content_type="text/plain")

        if (
            request.path_info == "/"
            and request.method == "HEAD"
            and user_agent.startswith("Go-http-client")
        ):
            return HttpResponse("", content_type="text/plain")

        return self.get_response(request)
