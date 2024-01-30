from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/auth/', include('App_Auth.urls')),
    path('api/boards/', include('App_Boards.urls')),
    path('api/pins/', include('App_Pins.urls')),
    path('api/profiles/', include('App_Profiles.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)