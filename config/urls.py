from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

django_urlpatterns = [
    path('admin/', admin.site.urls),
]

third_party_urlpatterns = [
    # API Documentation (Spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

local_urlpatterns = [
    path('', include('apps.accounts.urls')),
    path('', include('apps.teams.urls')),
]

urlpatterns = (
    django_urlpatterns
    + third_party_urlpatterns
    + local_urlpatterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
