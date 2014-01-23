from django.conf import settings
from django.template.loader import render_to_string

def analytics(request):
    """
    Returns Google analytics code.
    """
    if not settings.DEBUG:
        return { 'analytics_code': render_to_string("analytics.html", { 'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY }) }
    else:
        return { 'analytics_code': "" }

def uservoice(request):
    """
    Returns Uservoice feedback box code.
    """
    if not settings.DEBUG:
        return { 'uservoice_code': render_to_string("uservoice.html", {}) }
    else:
        return { 'uservoice_code': "" }
