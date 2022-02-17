from django.urls import path
from django.views.generic import RedirectView

from webapp.views.task import IndexView, TaskView, UpdateTask, DeleteTask
from webapp.views.project import IndexProject, ProjectView, ProjectCreate, ProjectCreateTask, ProjectUpdate, ProjectDelete, ProjectGetUser

app_name = "webapp"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("project/", RedirectView.as_view(pattern_name="project")),
    path("task/<int:pk>/", TaskView.as_view(), name="task_view"),
    path("task/<int:pk>/update/", UpdateTask.as_view(), name="update"),
    path("task/<int:pk>/delete/", DeleteTask.as_view(), name="delete"),
    path("projects/", IndexProject.as_view(), name="project"),
    path("project/<int:pk>/tasks/", ProjectView.as_view(), name="project_view"),
    path("project/create/", ProjectCreate.as_view(), name="project_create"),
    path("project/<int:pk>/create/task/", ProjectCreateTask.as_view(), name="create_task"),
    path("project/<int:pk>/update/", ProjectUpdate.as_view(), name="project_update"),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name="project_delete"),
    path("project/<int:pk>/add/user/", ProjectGetUser.as_view(), name="project_add_user")
]