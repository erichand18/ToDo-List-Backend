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
            username_to_check = request.POST.get('username')

            if not username_to_check:
                # Bad request. No username came with the request. Send back a 422 with message
                response_body = {
                    'message': 'Error! No username submitted with request'
                }
                return JsonResponse(response_body, status=422)

            # Check that the username is in an acceptable format
            name_format = re.compile(r'^[ A-Za-z0-9_@./#&+-]*$')
            acceptable_name_format = name_format.match(username_to_check)

            if not acceptable_name_format:
                # username is not an acceptable format, so return a 422 with message
                response_body = {
                    'message': 'The username is not in the valid format'
                }
                return JsonResponse(response_body, status=422)
            else:
                # username is correct format, so check to see if the username is available
                account_matching_username = User.objects.filter(
                    username=username_to_check)

                username_is_available = len(account_matching_username) == 0

                response_body = {
                    'message': 'Successfully checked availability',
                    'available': bool(username_is_available)
                }
                return JsonResponse(response_body, status=200)
        else:
            response_body = {
                'message': 'Endpoint does not exists for this HTTP verb'
            }
            return JsonResponse(response_body, status=404)

# Look into Django native user auth


def user_login(request):
    return HttpResponse('Logged user in')


class TaskListView(ListView):
    def get(request):
        if request.method == 'GET':
            # Fetch tasks from the DB and except any errors
            try:
                task_list = list(Task.objects.values())

                return JsonResponse(
                    {
                        'message': 'Success',
                        'tasks': task_list,
                    },
                    status=200,
                )
            except Exception as error:
                return JsonResponse(
                    {
                        'message': f'An error occurred retrieving tasks: {error}',
                        'tasks': None
                    },
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb'
                },
                status=404,
            )


class TaskCreateView(ListView):
    @csrf_exempt
    def create(request):
        if request.method == 'POST':
            # TODO: Add data validation function
            # Example: end_date > start_date, all data present, length limits on data fields
            task_data = dict(request.POST.items())

            new_task = Task(
                user_id=task_data['user_id'],
                task_name=task_data['name'],
                task_description=task_data['description'],
                color=task_data['color'],
                date_created=task_data['date_created'],
                start_date=task_data['start_date'],
                end_date=task_data['end_date'],
            )

            new_task.save()

            return JsonResponse(
                {
                    'message': 'Successfully created task'
                },
                status=201
            )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb'
                },
                status=404
            )


class TaskDeleteView(ListView):
    @csrf_exempt
    def delete(request, task_id=0):
        # Delete a task
        if request.method == 'DELETE':
            try:
                task_to_delete = Task.objects.filter(id=task_id)
            except Exception as Error:
                # Failed to query for resource
                return JsonResponse({'message': 'Error deleting task!'}, status=500)

            # Check to make sure only one task was found
            task_count = len(list(task_to_delete))

            if task_count > 1:
                # More than one task found for one pk. Throw an error and don't try to delete
                return JsonResponse(
                    {
                        'message': 'Error! More than one task found while trying to delete a task'
                    },
                    status=500
                )

            elif task_count == 0:
                # No records found, so nothing to delete
                return JsonResponse(
                    {
                        'message': 'No task found!'
                    },
                    status=404
                )

            else:
                # One record found as expected, so attempt to delete the resource
                try:
                    task_to_delete.delete()

                    return JsonResponse(
                        {
                            'message': 'Successfully deleted task'
                        },
                        status=200
                    )
                except Exception as error:
                    # failed to delete resource
                    return JsonResponse({'message': 'Error deleting task!'}, status=500)
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb'
                },
                status=404
            )


class TaskEditView(ListView):
    def edit(request, task_id):
        if request.method == 'PUT':
            # Find the record to update
            try:
                task_to_update = Task.objects.filter(pk=task_id)
            except Exception as error:
                return JsonResponse(
                    {
                        'message': 'Error finding task to update',
                        'error': error
                    },
                    status=500,
                )

            # Make sure only one record was found
            if len(list(task_to_update)) == 1:
                updates = dict(request.PUT.items())

                # TODO: validate updates

                for key in updates:
                    task_to_update[key] = updates[key]

                try:
                    task_to_update.save()
                except Exception as error:
                    return JsonResponse(
                        {
                            'message': 'Error updating task',
                            'error': error
                        },
                        status=500,
                    )
            else:
                return JsonResponse(
                    {
                        'message': 'error updating task'
                    },
                    status=500
                )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb'
                },
                status=404
            )


class TaskShareView(ListView):
    def share(request):
        if request.method == 'POST':
            return JsonResponse('Shared the task list')
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb'
                },
                status=404
            )
