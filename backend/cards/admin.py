from django.contrib import admin
from .models import Flashcard, Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
    search_fields = ('name',)

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('front', 'subject', 'order', 'last_seen')
    list_filter = ('subject', 'last_seen')
    search_fields = ('front', 'back')
    ordering = ('order',)
