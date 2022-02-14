from django.contrib import admin

from .models import Message, Post


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ('sender', 'recipient', 'content', 'post')
    list_display = ('sender', 'recipient', 'date', 'content')
    list_filter = ('date', 'sender', 'recipient')
    ordering = ('-date',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'category', 'header', 'text')
    list_display = ('header', 'date', 'author', 'category')
    list_filter = ('date', 'author', 'category')
    ordering = ('-date',)
