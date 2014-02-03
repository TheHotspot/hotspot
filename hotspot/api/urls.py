from django.conf.urls import patterns, include, url
import views

### Favored API for Hotspot-made apps to access internal data

urlpatterns = patterns('',
    url(r'^$', views.docs),
    url(r'^hotspots', views.hotspots),
    url(r'^checkin', views.checkin),
)
