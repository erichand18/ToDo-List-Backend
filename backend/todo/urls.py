from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/user/name/available', views.username_available,
         name='user-name-available'),
    path('/user/login', views.user_login, name='user-login'),
    path('/task/list', views.task_list, name='task-list'),
    path('/task/new', views.task_create, name='task-create'),
    path('/task/:id/edit', views.task_edit, name='task-edit'),
    path('/task/:id/delete', views.task_delete, name='task-delete'),
]
