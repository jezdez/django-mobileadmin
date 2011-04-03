from django.conf.urls.defaults import *
import mobileadmin

urlpatterns = patterns('',
    (r'^(.*)', include(mobileadmin.sites.site.urls)),
)
