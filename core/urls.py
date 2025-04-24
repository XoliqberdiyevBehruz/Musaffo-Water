from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    info=openapi.Info(
        title="Musaffo Suv Crm",
        default_version='version 1',
        description='this is first version of musaffo water crm',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # url='https://behruz.repid.uz'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/common/', include('common.urls')),

   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
