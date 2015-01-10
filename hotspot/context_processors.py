from django.conf import settings
from django.template.loader import render_to_string

def get_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip

def analytics(request):
    """
    Returns segment.io analytics itegration code.
    """
    if not settings.DEBUG or settings.DEBUG_ANALYTICS:
        return { 'analytics_code': render_to_string("analytics.html", { 'segment_api_key': settings.SEGMENT_ANALYTICS_KEY}) }
    else:
        return { 'analytics_code': "" }
