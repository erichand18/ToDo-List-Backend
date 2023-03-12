from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    hashed_pw = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_created = models.DateTimeField()


class Task(models.Model):
    user = models.ForeignKey(
        User,
    )
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=4095)
    color = models.CharField(max_length=6)
    date_created = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Task_Share(models.Model):
    task = models.ForeignKey(
        Task,
    )
    sender_user = models.ForeignKey(
        User,
    )
    recipient_user = models.ForeignKey(
        User,
    )
    date_shared = models.DateTimeField()
    viewed = models.BooleanField()
