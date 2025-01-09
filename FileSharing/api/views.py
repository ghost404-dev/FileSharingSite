from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.views import APIView
from .models import File
from django.conf import settings
from .serializers import FileSerializer, UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated


class FileViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с файлами
    """
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        #Ограничение файлов для текущего пользователя
        return File.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        # Устанавливаем текушего пользователя при создании файла
        serializer.save(user=self.request.user)

class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, file_id):
        try:
            file = File.objects.get(id=file_id, user=request.user)
            file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except file.DoesNotExist:
            return Response({"detail: Файл не найден или вы не владелец файла."},status=status.HTTP_404_NOT_FOUND)

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            file = File.objects.get(id=file_id, user=request.user)
            file_path = file.file.path  # Путь до файла в файловой системе
            response = FileResponse(open(file_path, 'rb'))
            return response
        except File.DoesNotExist:
            return Response({"detail": "Файл не найден или вы не владелец файла."}, status=status.HTTP_404_NOT_FOUND)

class UserRegisterView(APIView):
    def  post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"massage": "Пользователь зарегистрирован!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    