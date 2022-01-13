from django import forms
from django.forms import widgets

from webapp.models import Type, Status


class TaskForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label="Название")
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label="New", label="Статус")
    type = forms.ModelChoiceField(queryset=Type.objects.all(), empty_label="Task", label="Тип")
    description = forms.CharField(max_length=2000, required=True, label="Описание",
                              widget=widgets.Textarea(attrs={"rows": 5, "cols":50}))
