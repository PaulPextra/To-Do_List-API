from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo')
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    @property
    def user_name(self):
        return self.user.first_name
