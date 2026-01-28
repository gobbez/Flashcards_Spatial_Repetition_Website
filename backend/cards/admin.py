from django.contrib import admin
from .models import Flashcard, Subject, Quiz

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'moltiplicator')
    search_fields = ('name',)
    ordering = ('-points',)

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('front', 'subject', 'order', 'last_seen')
    list_filter = ('subject', 'last_seen')
    search_fields = ('front', 'back')
    ordering = ('order',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'subject', 'points')
    list_filter = ('subject',)
    search_fields = ('question',)
