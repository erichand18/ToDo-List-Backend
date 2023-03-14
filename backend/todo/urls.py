from django.urls import path

from . import views

urlpatterns = [
    path('user/name/available', views.UsernameAvailabilityView.is_available,
         name='user-name-available'),
    path('user/login', views.user_login, name='user-login'),
    path('task/list', views.TaskListView.get, name='task-list'),
    path('task/new', views.TaskCreateView.create, name='task-create'),
    path(r'task/(?P<task_id>[0-9])/edit', views.task_edit, name='task-edit'),
    path(r'task/(?P<task_id>[0-9])/delete',
         views.task_delete, name='task-delete'),
]

# Need to format this better. Want to add save-on-edit rule to put one function parameter per line when you append ',' to the last
# parameter.
