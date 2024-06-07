from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/", include("config.api_router"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
