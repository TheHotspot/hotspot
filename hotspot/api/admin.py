from django.contrib import admin

# Register your models here.

import models as api

admin.site.register(api.Hotspot)
admin.site.register(api.Business)
admin.site.register(api.CheckIn)