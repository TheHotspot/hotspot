import xadmin

# Register your models here.

import models as api

xadmin.site.register(api.Hotspot)
xadmin.site.register(api.Business)
xadmin.site.register(api.CheckIn)
