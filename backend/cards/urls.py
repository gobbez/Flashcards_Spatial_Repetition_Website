from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlashcardViewSet, SubjectViewSet, QuizViewSet

router = DefaultRouter()
router.register(r'flashcards', FlashcardViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'quizzes', QuizViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
