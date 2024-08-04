from django.conf import settings as django_setting
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from users.api.auth import login, login_refresh, logout, whoami
from rest_framework.routers import SimpleRouter

from users.api.support_app import DocumentAPI

schema_view = get_schema_view(
    openapi.Info(
        title="Himalayan Trail Running API",
        default_version='v1',
        description="",
        terms_of_service="",
        contact=openapi.Contact(email="himalayancreatives.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
router = SimpleRouter()

router.register('documents', DocumentAPI)

api_version_1 = [
    path('app/auth/refresh/', login_refresh),
    path('app/auth/logout/', logout),
    path('app/auth/', login),
    path('app/whoami/', whoami),
    path('app/', include(router.urls)),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('sales/', include('pos.urls')),
    path('content/', include('content.urls'))
]

urlpatterns = [
    path("api/docs/",
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/', include(api_version_1)),
]
urlpatterns += static(django_setting.MEDIA_URL,
                      document_root=django_setting.MEDIA_ROOT)
urlpatterns += static(django_setting.STATIC_URL,
                      document_root=django_setting.STATIC_ROOT)
urlpatterns += [path('', admin.site.urls)]
