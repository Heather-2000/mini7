from django.db import models
from login.models import User


class Talk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class TalkItem(models.Model):
    # talk_id = models.ForeignKey(Talk, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
