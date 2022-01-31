from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse
from django.db.models import Q
from webapp.forms import SearchForm

from webapp.models import Task, Status, Type, Project

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