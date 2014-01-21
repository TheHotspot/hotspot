"""
WSGI config for hotspot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

path = '/opt/hotspot'
if path not in sys.path:
   sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotspot.settings")

import django.views.debug

def null_technical_500_response(request, exc_type, exc_value, tb):
    raise exc_type, exc_value, tb
django.views.debug.technical_500_response = null_technical_500_response

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(app, evalex=True)
