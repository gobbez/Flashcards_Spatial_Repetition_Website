from rest_framework import serializers
from .models import Flashcard, Subject, Quiz

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'points']

class FlashcardSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = Flashcard
        fields = ['id', 'front', 'back', 'subject', 'subject_name', 'order', 'last_seen']

class QuizSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = Quiz
        fields = ['id', 'question', 'answer1', 'answer2', 'answer3', 'answer4', 'solution', 'subject', 'subject_name', 'points']
