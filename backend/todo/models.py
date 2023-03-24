from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=4095)
    color = models.CharField(max_length=6)
    date_created = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

    def toJson(self):
        return dict({
            'id': self.id,
            'user_id': self.user.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'color': self.color,
            'date_created': self.date_created,
            'completed': self.completed,
        })


class Task_Share(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )
    sender_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender_user',
    )
    recipient_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipient_user',
    )
    date_shared = models.DateTimeField()
    viewed = models.BooleanField()

    def __str__(self):
        return f"{self.sender_user} shared {self.task} with {self.recipient_user}"

    def toJson(self):
        return dict({
            'task_id': self.task.id,
            'sender_user_id': self.sender_user.id,
            'recipient_user_id': self.recipient_user.id,
            'date_shared': self.date_shared,
            'viewed': self.viewed,
        })
