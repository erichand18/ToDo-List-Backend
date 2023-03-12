from django.http import HttpResponse
from django.shortcuts import render


def username_available(request):
    return HttpResponse("Checked if username is available")


def user_login(request):
    return HttpResponse("Logged user in")


def task_list(request):
    return HttpResponse("Got the task list")


def task_create(request):
    return HttpResponse("Created a task")


def task_delete(request):
    return HttpResponse("Deleted a task")


def task_edit(request):
    return HttpResponse("Edited a task")


def share_task(request):
    return HttpResponse("Shared the task list")
