import uuid
from django.utils.timezone import now, timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import mimetypes


class File(models.Model):

    class FileType(models.TextChoices):
        IMAGE = 'image', _('Image')
        DOCUMENT = 'document', _('Document')
        AUDIO = 'audio', _('Audio')
        VIDEO = 'video', _('Video')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='user_files/')
    file_size = models.BigIntegerField(editable=False)  # Только для чтения
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255, editable=False)  # Только для чтения
    file_type = models.CharField(
        max_length=50,
        choices=FileType.choices,
        default=FileType.DOCUMENT,
        editable=False
    )
    shared_link = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_shared = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True, blank=True)
    link_expiry = models.DateTimeField(null=True, blank=True)  # Срок действия ссылки

    def __str__(self):
        return f'{self.filename} ({self.user.username})'
    
    def save(self, *args, **kwargs):
        # Генерируем имя файла, если оно не указано
        if not self.filename:
            self.filename = self.file.name.split('/')[-1]
        
        # Автоматически сохраняем размер файла
        self.file_size = self.file.size

        # Определяем тип файла на основе его расширения, если он не задан
        if not self.file_type:
            mime_type, encoding = mimetypes.guess_type(self.file.name)
            if mime_type:
                if mime_type.startswith('image'):
                    self.file_type = self.FileType.IMAGE
                elif mime_type.startswith('audio'):
                    self.file_type = self.FileType.AUDIO
                elif mime_type.startswith('video'):
                    self.file_type = self.FileType.VIDEO
                else:
                    self.file_type = self.FileType.DOCUMENT
            else:
                self.file_type = self.FileType.DOCUMENT

        super().save(*args, **kwargs)

    def set_link_expiry(self, duration):
        """
        Устанавливает срок действия ссылки.
        :param duration: 'infinite' или число минут.
        """
        if duration == 'infinite':
            self.link_expiry = None
        else:
            try:
                self.link_expiry = now() + timedelta(minutes=int(duration))
            except ValueError:
                raise ValueError("Duration must be 'infinite' or a valid integer.")

    def is_link_valid(self):
        """
        Проверяет, действительна ли ссылка.
        """
        if not self.is_shared:
            return False
        if self.link_expiry and now() > self.link_expiry:
            return False
        return True
    
    def get_file_url(self):
        if self.file:
            return self.file.url
        return None
