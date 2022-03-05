from django.contrib import admin

from .models import Response, Advert


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    fields = ('sender', 'recipient', 'content', 'post')
    list_display = ('sender', 'recipient', 'date', 'content')
    list_filter = ('date', 'sender', 'recipient')
    ordering = ('-date',)


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    fields = ('author', 'category', 'header', 'content')
    list_display = ('header', 'date', 'author', 'category')
    list_filter = ('date', 'author', 'category')
    ordering = ('-date',)
