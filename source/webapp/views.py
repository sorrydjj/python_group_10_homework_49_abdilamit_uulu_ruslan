import datetime

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, FormView
from django.urls import reverse

from webapp.models import Task, Status, Type

from webapp.forms import TaskForm

from webapp.base import FormView as CustomFormView


class IndexView(TemplateView):
    template_name = "index.html"
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

class CreateTask(CustomFormView):
    form_class = TaskForm
    template_name = "create_task.html"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("index_view", pk=self.object.pk)


class UpdateTask(FormView):
    form_class = TaskForm
    template_name = "update_task.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super(UpdateTask, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def get_initial(self):
        initial = {}
        for key in 'summary', 'stats', 'description':
            initial[key] = getattr(self.task, key)
        initial['types'] = self.task.types.all()
        return initial

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index_view', kwargs={"pk": self.task.pk})

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get("pk"))


class DeleteTask(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        return render(request, "delete_task.html", {"task": task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        task.delete()
        return redirect('index')