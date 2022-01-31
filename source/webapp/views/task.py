from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse

from webapp.models import Task, Status, Type

from webapp.forms import TaskForm, SearchForm

from webapp.base import FormView as CustomFormView


class IndexView(ListView):
    template_name = "tasks/index.html"
    model = Task
    context_object_name = "tasks"
    paginate_by = 10
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            print(self.search_value)
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("-updated_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['form'] = SearchForm(initial={"search": self.search_value})
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")

    # def get_queryset(self):
    #     queryset = super(IndexView, self).get_queryset()
    #     return queryset.order_by('-updated_at')
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(IndexView, self).get_context_data(object_list=object_list, **kwargs)
    #     print(context)
    #     return context

    # def get(self, request, *args, **kwargs):
    #     task = Task.objects.order_by("created_at")
    #     context = {"task": task}
    #     return render(request, 'index.html', context)

class TaskView(TemplateView):
    template_name = "tasks/view.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get("pk"))

        context['task'] = task
        return context

class CreateTask(CustomFormView):
    form_class = TaskForm
    template_name = "tasks/create.html"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("index_view", pk=self.object.pk)


class UpdateTask(FormView):
    form_class = TaskForm
    template_name = "tasks/update.html"

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
        return render(request, "tasks/delete.html", {"task": task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        task.delete()
        return redirect('index')