from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^api/', include('authenticate.urls')),
    url(r'^api/', include('app.user.urls')),
    url(r'^api/', include('app.order.urls')),
    url(r'^api/', include('app.job.urls')),
    url(r'^api/', include('app.setting.urls')),
    url(r'^api/', include('app.generic.urls')),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)