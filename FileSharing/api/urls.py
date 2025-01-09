from rest_framework.routers import DefaultRouter
from .views import FileViewSet, UserRegisterView
from django.urls import path

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = router.urls

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
]