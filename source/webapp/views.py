from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from webapp.models import Task, Status, Type


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