#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings
import decompile.views as disview

urlpatterns = patterns('',
    (r'^$', disview.index), 
    (r'^get_result/$', disview.get),
    (r'^excute/$', disview.excute),
    (r'^restore_vm/$', disview.restore_vm),
    (r'^exit/$', disview.exit),
    (r'^next_step/$', disview.next_step),
    
    (r'^cobramedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH}),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
