# models.py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # No need to limit content for display
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
