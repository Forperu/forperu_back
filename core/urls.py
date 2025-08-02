from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.api_urls import api_urlpatterns

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include("apps.users.urls")),
  path('api/', include(api_urlpatterns)),
  path('api/', include("apps.companies.urls")),
  path('api/', include("apps.products.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)