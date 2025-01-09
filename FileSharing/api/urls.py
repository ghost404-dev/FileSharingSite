from rest_framework.routers import DefaultRouter
from .views import FileViewSet, UserRegisterView, FileDeleteView, FileDownloadView
from django.urls import path

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = router.urls

urlpatterns += [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('files/<int:file_id>/delete/', FileDeleteView.as_view(), name='file-delete'),
    path('files/<int:file_id>/download/', FileDownloadView.as_view(), name='file-download'),
]