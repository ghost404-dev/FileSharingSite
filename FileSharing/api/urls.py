from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, UserRegisterView, FileDeleteView, FileDownloadView
from django.urls import path


# Настройка схемы
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v0.0.1',
        description="Документация для вашего API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="trueface0rmrf0@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = router.urls

urlpatterns += [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('files/<int:file_id>/delete/', FileDeleteView.as_view(), name='file-delete'),
    path('files/<int:file_id>/download/', FileDownloadView.as_view(), name='file-download'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]