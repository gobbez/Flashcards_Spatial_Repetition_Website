from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlashcardViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'flashcards', FlashcardViewSet)
router.register(r'subjects', SubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
