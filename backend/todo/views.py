from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.middleware import csrf
from todo.models import Task, Task_Share
from django.http import JsonResponse, QueryDict
import re
from datetime import datetime
import jwt
import json
import environ

env = environ.Env()
environ.Env.read_env()


class UsernameAvailabilityView(ListView):
    def is_available(request):
        if request.method == 'POST':
            username_to_check = request.POST.get('username')

            if not username_to_check:
                # Bad request. No username came with the request. Send back a 422 with message
                return JsonResponse(
                    {
                        'message': 'Error! No username submitted with request',
                    },
                    status=422,
                )

            # Check that the username is in an acceptable format
            name_format = re.compile(r'^[ A-Za-z0-9_@./#&+-]*$')
            acceptable_name_format = name_format.match(username_to_check)

            if not acceptable_name_format:
                # username is not an acceptable format, so return a 422 with message
                return JsonResponse(
                    {
                        'message': 'The username is not in the valid format',
                    },
                    status=422,
                )
            else:
                # username is correct format, so check to see if the username is available
                account_matching_username = User.objects.filter(
                    username=username_to_check
                )

                username_is_available = len(account_matching_username) == 0

                return JsonResponse(
                    {
                        'message': 'Successfully checked availability',
                        'available': bool(username_is_available),
                    },
                    status=200,
                )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404,
            )


class UserSignupView(ListView):
    def signup(request):
        if request.method == 'POST':
            # get user data from the request
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if not username or not email or not password or not first_name or not last_name:
                return JsonResponse(
                    {
                        'message': 'Missing data from user',
                    },
                    status=400
                )

            try:
                # Create user in the database
                user = User.objects.create_user(
                    username,
                    email,
                    password,
                    first_name=first_name,
                    last_name=last_name,
                )

                user.save()

                return JsonResponse(
                    {
                        'message': 'User successfully created!',
                    },
                    status=201,
                )
            except Exception as error:
                return JsonResponse(
                    {
                        'message': f'Error creating user: {error}',
                    },
                    status=500
                )

        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404,
            )


class UserLoginView(ListView):
    def user_login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Try to find the user
            try:
                user = User.objects.get(username=username)
            except Exception as error:
                return JsonResponse(
                    {
                        'message': f'Username does not exist: {error}',
                    },
                    status=400,
                )

            user = authenticate(request, username=username, password=password)

            if user is not None:
                bearer_token = jwt.encode(
                    {
                        'user_id': user.id,
                    },
                    env('JWT_SECRET'),
                    algorithm=env('JWT_ALGORITHM'),
                )
                return JsonResponse(
                    {
                        'message': 'Success',
                        'bearer_token': bearer_token,
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {
                        'message': 'Could not authenticate user!',
                    },
                    status=403,
                )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404,
            )


class TaskListView(ListView):
    def get(request):
        if request.method == 'GET':
            try:
                user_id = request.user.id

                # Get list of task_ids for tasks shared with the user
                task_share_data = Task_Share.objects.filter(
                    recipient_user=user_id
                ).filter(
                    viewed=False
                )

                shared_tasks_list = list(task_share_data)
                for task in shared_tasks_list:
                    task = task.toJson()

                # Fetch tasks the user has that were shared to the user
                shared_task_ids = [x.id for x in shared_tasks_list]

                shared_tasks = Task.objects.filter(
                    pk__in=shared_task_ids
                )

                shared_tasks_json = [x.toJson() for x in shared_tasks]

                # Fetch tasks from the DB and except any errors
                task_list = list(Task.objects.filter(
                    user_id=user_id
                ).exclude(
                    pk__in=shared_task_ids
                ))

                task_list_json = [x.toJson() for x in task_list]

                return JsonResponse(
                    {
                        'message': 'Success',
                        'tasks': task_list_json,
                        'shared_tasks': shared_tasks_json,
                    },
                    status=200,
                )
            except Exception as error:
                return JsonResponse(
                    {
                        'message': f'An error occurred retrieving tasks: {error}',
                        'tasks': None,
                    },
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404,
            )


class TaskCompleteView(ListView):
    def complete(request):
        if request.method == 'POST':
            user_id = request.user.id
            task_id = request.POST.get('task_id')

            try:
                # Fetch tasks from the DB and except any errors
                task = Task.objects.get(user_id=user_id, id=task_id)
                current_complete_status = task.completed

                task.completed = bool(not current_complete_status)
                task.save()

                return JsonResponse(
                    {
                        'message': 'task updated successfully',
                        'completed': task.completed,
                    }
                )
            except Exception as error:
                return JsonResponse(
                    {
                        'message': f'An error occurred completing task',
                    },
                    status=500,
                )

        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404,
            )


class TaskCreateView(ListView):
    def create(request):
        if request.method == 'POST':
            # TODO: Add data validation function
            # Example: end_date > start_date, all data present, length limits on data fields
            task_data = dict(request.POST.items())

            new_task = Task(
                user_id=request.user.id,
                task_name=task_data['name'],
                task_description=task_data['description'],
                date_created=datetime.now(),
            )

            new_task.save()

            return JsonResponse(
                {
                    'message': 'Successfully created task',
                },
                status=201,
            )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404,
            )


class TaskDeleteView(ListView):
    def delete(request, task_id=0):
        # Delete a task
        if request.method == 'DELETE':
            try:
                task_to_delete = Task.objects.filter(id=task_id)
            except Exception as Error:
                # Failed to query for resource
                return JsonResponse(
                    {
                        'message': 'Error deleting task!',
                    },
                    status=500,
                )

            # Check to make sure only one task was found
            task_count = len(list(task_to_delete))

            if task_count > 1:
                # More than one task found for one pk. Throw an error and don't try to delete
                return JsonResponse(
                    {
                        'message': 'Error! More than one task found while trying to delete a task',
                    },
                    status=500,
                )

            elif task_count == 0:
                # No records found, so nothing to delete
                return JsonResponse(
                    {
                        'message': 'No task found!',
                    },
                    status=404,
                )

            else:
                # One record found as expected, so attempt to delete the resource
                try:
                    task_to_delete.delete()

                    return JsonResponse(
                        {
                            'message': 'Successfully deleted task',
                        },
                        status=200,
                    )
                except Exception as error:
                    # failed to delete resource
                    return JsonResponse(
                        {
                            'message': 'Error deleting task!'
                        },
                        status=500,
                    )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404,
            )


class TaskEditView(ListView):
    def edit(request, task_id):
        if request.method == 'PUT':
            # Find the record to update
            try:
                task_to_update = Task.objects.filter(pk=task_id)

                updates = dict(QueryDict(request.body))
                # TODO: validate updates

                for key in updates:
                    updates[key] = updates[key][0]

                task_to_update.update(**updates)

                return JsonResponse(
                    {
                        'message': 'Successfully updated task',
                    },
                    status=200,
                )
            except Exception as error:
                return JsonResponse(
                    {
                        'message': 'Error finding task to update',
                        'error': error,
                    },
                    status=500,
                )

            except Exception as error:
                return JsonResponse(
                    {
                        'message': 'Error updating task',
                        'error': error,
                    },
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb',
                },
                status=404
            )


class TaskShareView(ListView):
    def share(request):
        if request.method == 'POST':
            task_id = request.POST.get('task_id')
            recipient_username = request.POST.get('recipient_username')

            # Find task to share
            task_to_share = Task.objects.get(pk=task_id)

            # Find user to share to and confirm they exist
            recipient_user = User.objects.get(username=recipient_username)

            if not recipient_user:
                return JsonResponse(
                    {
                        'message': 'Could not find user to share task with',
                    },
                    status=404,
                )
            elif not task_to_share:
                return JsonResponse(
                    {
                        'message': 'Could not find task to share',
                    },
                    status=404,
                )
            else:
                try:
                    # Create new task for recipient user
                    new_task = Task(
                        user_id=recipient_user.id,
                        task_name=task_to_share.task_name,
                        task_description=task_to_share.task_description,
                        date_created=datetime.now(),
                    )

                    new_task.save()

                    # Share the task
                    Task_Share.objects.create(
                        task_id=task_id,
                        sender_user=request.user,
                        recipient_user=recipient_user,
                        date_shared=datetime.now(),
                        viewed=False,
                    )

                    return JsonResponse(
                        {
                            'message': 'Successfully shared task',
                        },
                        status=200
                    )
                except Exception as error:
                    return JsonResponse(
                        {
                            'message': 'Failed to share task',
                            'error': error,
                        },
                        status=400
                    )

        else:
            return JsonResponse(
                {
                    'message': 'Endpoint does not exists for this HTTP verb'
                },
                status=404
            )
