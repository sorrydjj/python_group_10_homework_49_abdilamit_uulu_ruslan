import datetime

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from webapp.models import Task, Status, Type

from webapp.forms import TaskForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.order_by("created_at")
        context = {"task": task}
        return render(request, 'index.html', context)

class TaskView(TemplateView):
    template_name = "index_view.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        context['task'] = task
        return context

class CreateTask(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'create_task.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("title")
            status = form.cleaned_data.get("status")
            type = form.cleaned_data.get("type")
            description = form.cleaned_data.get("description")
            new_task = Task.objects.create(summary=name, stats=status, description=description, types=type)
            return redirect("index_view", pk=new_task.pk)
        return render(request, 'create_task.html', {"form": form})

class UpdateTask(View):

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        form = TaskForm(initial={
            'title': task.summary,
            'description': task.description,
            'status': task.stats,
            'type': task.types
        })
        return render(request, 'update_task.html', {"form": form})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.summary = form.cleaned_data.get("title")
            task.stats = form.cleaned_data.get("status")
            task.types = form.cleaned_data.get("type")
            task.description = form.cleaned_data.get("description")
            task.updated_at = datetime.datetime.now()
            task.save()
            return redirect("index_view", pk=task.pk)
        return render(request, 'update_task.html', {"task": task, "form": form})


class DeleteTask(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        return render(request, "delete_task.html", {"task": task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        task.delete()
        return redirect('index')