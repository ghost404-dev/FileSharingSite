from django.contrib import admin
from .models import User, File

@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('username','password','email') 
    list_filter = ('username',)

@admin.register(File)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user','filename','file_type') 
    list_filter = ('user',)