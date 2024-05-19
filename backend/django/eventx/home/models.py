from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_id = models.IntegerField()
    api_key = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.user.username} - {self.api_key}'