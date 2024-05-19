from django.db import models
from django.contrib.auth.models import User
import hashlib
import time

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_id = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.user.username} - {self.api_key}'

    def generate_event_id(self):
        timestamp = int(time.time())
        unique_string = f"{self.user.username}-{self.event_name}-{timestamp}"
        event_id = hashlib.sha256(unique_string.encode()).hexdigest()[:10]
        return event_id
    
    def save(self, *args, **kwargs):
        # Generate event_id only if it's not already set
        if not self.event_id:
            self.event_id = self.generate_event_id()
        super().save(*args, **kwargs)
