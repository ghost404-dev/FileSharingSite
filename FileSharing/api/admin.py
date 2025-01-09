from django.contrib import admin
from .models import File


@admin.register(File)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user','filename','file_type') 
    list_filter = ('user',)