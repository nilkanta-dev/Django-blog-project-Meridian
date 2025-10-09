

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView
from django.contrib.auth.decorators import login_required
from core.views import SwaggerView
    


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('core.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema',SpectacularAPIView.as_view(),name='schema'),
    path('api/docs/',SwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path("", include('core.urls')),
    path('tinymce/', include('tinymce.urls')),
    path("", include('userprofiles.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
