from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import FileResponse, HttpResponse
from rest_framework.views import APIView
from .models import File
from rest_framework.decorators import api_view, permission_classes
from .serializers import FileSerializer, UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_link(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)

    # Настройки ссылки
    duration = request.data.get('duration', 'infinite')  # '1', '5', 'infinite'
    password = request.data.get('password', None)

    file.is_shared = True
    file.password = password
    file.set_link_expiry(duration)
    file.save()

    return Response({
        "message": "Ссылка успешно создана",
        "shared_link": f"/api/files/{file.shared_link}/shared/"
    })


@api_view(['GET'])
def access_shared_file(request, shared_link):
    # Находим файл по shared_link
    file = get_object_or_404(File, shared_link=shared_link)

    # Проверяем, действительна ли ссылка
    if not file.is_link_valid():
        return Response({"error": "Ссылка недействительна или срок действия истёк"}, status=403)

    # Проверяем пароль, если он установлен
    password = request.query_params.get('password', None)
    if file.password and file.password != password:
        return Response({"error": "Неверный пароль"}, status=403)

    # Подготавливаем файл для скачивания
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
    return response