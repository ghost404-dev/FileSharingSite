from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import File
from .serializers import FileSerializer, UserRegisterSerializer


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

class UserRegisterView(APIView):
    def  post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"massage": "Пользователь зарегистрирован!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    