from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.points})"

class Flashcard(models.Model):
    front = models.TextField()
    back = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='cards')
    order = models.FloatField(help_text="Order determines the sequence. Lower comes first.")
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.front[:30]}... ({self.subject.name})"
