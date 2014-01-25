from django.contrib import admin

# Register your models here.

import models as api

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'telephone')

class HotspotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'score', 'nickname', 'business', 'description', 'LAT', 'LNG',  'capacity', 'telephone', 'admins', 'checkins_recent')

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotspots', 'checkins_recent')

class CheckInAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotspot', 'time_in', 'time_out', 'length', 'is_checkedin')

admin.site.register(api.User, UserAdmin)
admin.site.register(api.Hotspot, HotspotAdmin)
admin.site.register(api.Business, BusinessAdmin)
admin.site.register(api.CheckIn, CheckInAdmin)
