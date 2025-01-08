from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.username

class File(models.Model):

    class FileType(models.TextChoices):
        IMAGE = 'image', _('Image')
        DOCUMENT = 'document', _('Document')
        AUDIO = 'audio', _('Audio')
        VIDEO = 'video', _('Video')

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', max_length=100)  # Путь к файлам
    upload_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=50, blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=FileType.choices, default=FileType.DOCUMENT)

    def __str__(self):
        return f'{self.filename} ({self.user.username})'
    
    def save(self, *args, **kwargs):
        # Генерируем filename из имени файла, если оно пустое
        if not self.filename:
            self.filename = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)