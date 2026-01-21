from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Flashcard, Subject
from .serializers import FlashcardSerializer, SubjectSerializer
from django.shortcuts import get_object_or_404
import math

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
        # Get all cards ordered (excluding current one to simulate queue)
        # We need the queue *as if this card was removed and placed elsewhere*
        # Actually, simpler: Get all cards, find where to insert.
        
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

        # Calculate new order value
        # We want to insert at `target_index`. 
        # So it should be between all_cards[target_index-1] and all_cards[target_index]
        # But wait, python lists are 0-indexed.
        # If target_index is 0, we want it at the VERY FRONT? No, "after 10 cards" means index 10 (0 to 9 are 10 cards).
        # So target_index 10 means it will be the 11th card.
        
        # Correction: list has `count` items. indices 0 to count-1.
        # unique insert positions: 0 (head) to count (tail).
        
        new_order = 0.0
        
        if count == 0:
            new_order = 1.0
        elif target_index >= count:
            # End of list
            new_order = all_cards[-1].order + 10.0
        elif target_index == 0:
            # Start of list (should generally not happen with "after X")
            new_order = all_cards[0].order / 2.0
        else:
            # Between prev and next
            prev_order = all_cards[target_index - 1].order
            next_order = all_cards[target_index].order
            new_order = (prev_order + next_order) / 2.0

        card.order = new_order
        card.save()

        return Response(FlashcardSerializer(card).data)
