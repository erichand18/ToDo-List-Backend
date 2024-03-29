from django.urls import path, re_path

from . import views

urlpatterns = [
    path(
        'user/name/available',
        views.UsernameAvailabilityView.is_available,
        name='user-name-available'
    ),
    path(
        'user/signup',
        views.UserSignupView.signup,
        name='user-signup'
    ),
    path(
        'user/login',
        views.UserLoginView.user_login,
        name='user-login'
    ),
    path(
        'task/list',
        views.TaskListView.get,
        name='task-list'
    ),
    path(
        'task/complete',
        views.TaskCompleteView.complete,
        name='task-complete'
    ),
    path(
        'task/new',
        views.TaskCreateView.create,
        name='task-create'
    ),
    path(
        'task/<int:task_id>/edit',
        views.TaskEditView.edit,
        name='task-edit',
    ),
    path(
        'task/<int:task_id>/delete',
        views.TaskDeleteView.delete,
        name='task-delete'
    ),
    path(
        'task/share',
        views.TaskShareView.share,
        name='task-share'
    ),
]

# Need to format this better. Want to add save-on-edit rule to put one function parameter per line when you append ',' to the last
# parameter.
