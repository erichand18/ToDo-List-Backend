from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from todo.models import Task, User, Task_Share
from django.views.decorators.csrf import csrf_exempt
import re
import time
import json


class UsernameAvailabilityView(ListView):
    @csrf_exempt
    def is_available(request):
        if request.method == 'POST':
            username_to_check = request.POST.get("username")

            if not username_to_check:
                # Bad request. No username came with the request. Send back a 422 with message
                response_body = {
                    "message": "Error! No username submitted with request"
                }
                return JsonResponse(response_body, status=422)

            # Check that the username is in an acceptable format
            name_format = re.compile(r'^[ A-Za-z0-9_@./#&+-]*$')
            acceptable_name_format = name_format.match(username_to_check)

            if not acceptable_name_format:
                # username is not an acceptable format, so return a 422 with message
                response_body = {
                    "message": "The username is not in the valid format"
                }
                return JsonResponse(response_body, status=422)
            else:
                # username is correct format, so check to see if the username is available
                account_matching_username = User.objects.filter(
                    username=username_to_check)

                username_is_available = len(account_matching_username) == 0

                response_body = {
                    "message": "Successfully checked availability",
                    "available": bool(username_is_available)
                }
                return JsonResponse(response_body, status=200)
        else:
            response_body = {
                "message": "Endpoint does not exists for this HTTP verb"
            }
            return JsonResponse(response_body, status=404)

# TODO: Look into Django native user auth


def user_login(request):
    return HttpResponse("Logged user in")


class TaskListView(ListView):
    def get(request):
        if request.method == "GET":
            # Fetch tasks from the DB and except any errors
            try:
                task_list = list(Task.objects.values())

                response_body = {
                    "message": "Success",
                    "tasks": task_list,
                }

                return JsonResponse(response_body, status=200)
            except Exception as error:
                response_body = {
                    "message": f"An error occurred retrieving tasks: {error}",
                    "tasks": None
                }
                return JsonResponse(response_body, status=500)
        else:
            response_body = {
                "message": "Endpoint does not exists for this HTTP verb"
            }
            return JsonResponse(response_body, status=404)


class TaskCreateView(ListView):
    @csrf_exempt
    def create(request):
        if request.method == 'POST':
            # TODO: Add data validation function
            # Example: end_date > start_date, all data present, length limits on data fields
            task_data = dict(request.POST.items())

            print(task_data)
            new_task = Task(user_id=task_data["user_id"],
                            task_name=task_data["name"],
                            task_description=task_data["description"],
                            color=task_data["color"],
                            date_created=task_data["date_created"],
                            start_date=task_data["start_date"],
                            end_date=task_data["end_date"]
                            )
            new_task.save()

            response_body = {
                "message": ""
            }
            return JsonResponse(response_body, status=201)
        else:
            response_body = {
                "message": "Endpoint does not exists for this HTTP verb"
            }
            return JsonResponse(response_body, status=404)

# TODO: convert to class-based view


class TaskDeleteView(ListView):
    @csrf_exempt
    def delete(request):
        # Delete a task
        pass


def task_delete(request):
    return HttpResponse("Deleted a task")

# TODO: convert to class-based view


def task_edit(request):
    return HttpResponse("Edited a task")

# TODO: convert to class-based view


def share_task(request):
    return HttpResponse("Shared the task list")
