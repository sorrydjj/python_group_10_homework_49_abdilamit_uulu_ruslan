"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from webapp.views.task import IndexView, TaskView, UpdateTask, DeleteTask
from webapp.views.project import IndexProject, ProjectView, ProjectCreate, ProjectCreateTask, ProjectUpdate


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("task/<int:pk>/", TaskView.as_view(), name="index_view"),
    path("task/<int:pk>/update/", UpdateTask.as_view(), name="update"),
    path("task/<int:pk>/delete/", DeleteTask.as_view(), name="delete"),
    path("projects/", IndexProject.as_view(), name="project"),
    path("project/<int:pk>/tasks/", ProjectView.as_view(), name="project_view"),
    path("project/create/", ProjectCreate.as_view(), name="project_create"),
    path("project/<int:pk>/create/task/", ProjectCreateTask.as_view(), name="create_task"),
    path("project/<int:pk>/update/", ProjectUpdate.as_view(), name="project_update")
]
