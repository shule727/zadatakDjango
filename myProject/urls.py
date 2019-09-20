from django.urls import include, path
from django.contrib import admin
from instagram import urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include(urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
