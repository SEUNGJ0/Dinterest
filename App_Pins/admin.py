from django.contrib import admin
from .models import Pins, Comment, Like

@admin.register(Pins)
class PinsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_date', 'updated_data')
    search_fields = ['title', 'user__email']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'pin', 'text', 'created_date', 'updated_data')
    search_fields = ['text', 'user__email']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'pin')
    search_fields = ['user__email']
