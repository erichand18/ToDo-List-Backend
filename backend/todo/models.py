from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_picture = models.CharField(max_length=2048)
    date_created = models.DateTimeField()

    def __str__(self):
        return self.user.username


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=4095)
    color = models.CharField(max_length=6)
    date_created = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.task_name


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
