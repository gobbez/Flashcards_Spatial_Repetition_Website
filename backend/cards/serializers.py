from rest_framework import serializers
from .models import Flashcard, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'points']

class FlashcardSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = Flashcard
        fields = ['id', 'front', 'back', 'subject', 'subject_name', 'order', 'last_seen']
