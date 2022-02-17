from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse

from webapp.models import Task, Status, Type, Project, User

from webapp.forms import SearchForm, ProjectForm, ProjectAddUserForm
from webapp.forms import TaskForm


class IndexProject(ListView):
    template_name = "project/index.html"
    model = Project
    context_object_name = "project"
    paginate_by = 3
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            print(self.search_value)
            query = Q(name__icontains=self.search_value) | Q(descriptions__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("-date_start")

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


class ProjectView(DetailView):
    template_name = 'project/view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.filter(project__pk=self.object.pk)
        project = self.object
        context['task'] = task
        context['project'] = project
        context["users"] = project.users.all()
        return context


class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project/create.html"
    permission_required = "webapp.add_project"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.users.set((self.request.user, ))
        return redirect('webapp:project')

    def form_invalid(self, form):
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all()


class ProjectCreateTask(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "project/create_task.html"
    permission_required = "webapp.add_task"


    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.project = project
        self.object.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)

    def form_invalid(self, form):
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all()


class ProjectUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = "project/update.html"
    model = Project
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse("webapp:project")

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all()


class ProjectDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = "project/delete.html"
    permission_required = "webapp.delete_project"

    def post(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("webapp:project")

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all()


class ProjectGetUser(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectAddUserForm
    template_name = "project/add_user.html"
    permission_required = "webapp.change_project"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['users'] = User.objects.filter(pk__gt=1)
        return kwargs

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:project")