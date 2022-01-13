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