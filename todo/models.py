from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo', null=True, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} for {self.user.username}'
    
    
    def delete(self):
        self.is_active = False
        self.save()
        return
    
    @property
    def username(self):
        return self.user.username
