from django.contrib import admin

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))



# Register your models here.

import models as api

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'telephone')

class HotspotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'score', 'nickname', 'business', 'description', 'LAT', 'LNG',  'capacity', 'telephone', 'admins', 'checkins_recent')
    def merge(self, request, queryset):
        main = queryset[0]
        tail = [ x for x in queryset[1:]]
        final_hotspot = api.merge_objects(main, tail)
        #self.message_user(request, "Please manually fix any wrong data after the merge.")
        return HttpResponseRedirect("/admin/api/hotspot/%s" % final_hotspot.id)

    merge.short_description = "do not use: Merge selected hotspots into one"
    actions = [merge]

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hotspots', 'checkins_recent')

class CheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotspot', 'time_in', 'time_out', 'length', 'is_checkedin')

admin.site.register(api.User, UserAdmin)
admin.site.register(api.Hotspot, HotspotAdmin)
admin.site.register(api.Business, BusinessAdmin)
admin.site.register(api.CheckIn, CheckInAdmin)


