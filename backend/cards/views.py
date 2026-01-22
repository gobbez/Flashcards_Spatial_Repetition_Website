from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Flashcard, Subject, Quiz
from .serializers import FlashcardSerializer, SubjectSerializer, QuizSerializer
from django.shortcuts import get_object_or_404
import math
import random
import re

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        card = self.get_object()
        rating = request.data.get('rating')
        
        # Valid ratings
        if rating not in ['understood', 'so_so', 'study_more']:
            return Response({'error': 'Invalid rating'}, status=status.HTTP_400_BAD_REQUEST)

        # Update Subject points
        points_map = {
            'understood': 10,
            'so_so': 3,
            'study_more': 1
        }
        card.subject.points += points_map[rating]
        card.subject.save()

        # Reordering Logic
        all_cards = list(Flashcard.objects.exclude(id=card.id).order_by('order'))
        count = len(all_cards)
        
        target_index = 0
        if rating == 'study_more':
            target_index = min(10, count)
        elif rating == 'so_so':
            target_index = min(25, count)
        elif rating == 'understood':
            target_index = int(count * 0.9)
            if target_index >= count:
                target_index = count

        new_order = 0.0
        if count == 0:
            new_order = 1.0
        elif target_index >= count:
            new_order = all_cards[-1].order + 10.0
        elif target_index == 0:
            new_order = all_cards[0].order / 2.0
        else:
            prev_order = all_cards[target_index - 1].order
            next_order = all_cards[target_index].order
            new_order = (prev_order + next_order) / 2.0

        card.order = new_order
        card.save()

        return Response(FlashcardSerializer(card).data)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        file = request.FILES.get('file')
        subject_name = request.data.get('subject', 'General')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        content = file.read().decode('utf-8')
        subject, _ = Subject.objects.get_or_create(name=subject_name)
        
        # Parse flashcards
        # Format: 
        # F: "Front"
        # B: "Back"
        cards_data = re.findall(r'F:\s*"(.*?)"\s*B:\s*"(.*?)"', content, re.DOTALL)
        
        created_count = 0
        last_order = Flashcard.objects.all().order_by('-order').first()
        current_order = (last_order.order + 1.0) if last_order else 1.0
        
        for front, back in cards_data:
            Flashcard.objects.create(
                front=front,
                back=back,
                subject=subject,
                order=current_order
            )
            current_order += 1.0
            created_count += 1
            
        return Response({'message': f'Successfully uploaded {created_count} flashcards'})

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    @action(detail=False, methods=['get'])
    def random(self, request):
        quizzes = list(self.get_queryset())
        if not quizzes:
            return Response({'error': 'No quizzes available'}, status=status.HTTP_404_NOT_FOUND)
        quiz = random.choice(quizzes)
        return Response(self.get_serializer(quiz).data)

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        quiz = self.get_object()
        answer = request.data.get('answer')
        
        if answer is None:
            return Response({'error': 'No answer provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        is_correct = int(answer) == quiz.solution
        if is_correct:
            quiz.subject.points += quiz.points
            quiz.subject.save()
            
        return Response({
            'correct': is_correct,
            'solution': quiz.solution,
            'subject_points': quiz.subject.points
        })

    @action(detail=False, methods=['post'])
    def upload(self, request):
        file = request.FILES.get('file')
        subject_name = request.data.get('subject', 'General')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        content = file.read().decode('utf-8')
        subject, _ = Subject.objects.get_or_create(name=subject_name)
        
        # Format:
        # Q: "Question"
        # A1: "Ans 1"
        # A2: "Ans 2"
        # A3: "Ans 3"
        # A4: "Ans 4"
        # S: 1
        # P: 5 (optional, default to 1)
        quizzes_data = re.findall(r'Q:\s*"(.*?)"\s*A1:\s*"(.*?)"\s*A2:\s*"(.*?)"\s*A3:\s*"(.*?)"\s*A4:\s*"(.*?)"\s*S:\s*(\d+)(?:\s*P:\s*(\d+))?', content, re.DOTALL)
        
        created_count = 0
        for q, a1, a2, a3, a4, sol, pts in quizzes_data:
            Quiz.objects.create(
                question=q,
                answer1=a1,
                answer2=a2,
                answer3=a3,
                answer4=a4,
                solution=int(sol),
                subject=subject,
                points=int(pts) if pts else 1
            )
            created_count += 1
            
        return Response({'message': f'Successfully uploaded {created_count} quizzes'})
