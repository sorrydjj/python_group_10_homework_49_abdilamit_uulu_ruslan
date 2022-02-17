
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Type, Status, Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["project"]
        widgets = {
            "types": forms.CheckboxSelectMultiple
        }


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['description'] == cleaned_data['summary']:
            raise ValidationError("Text of the article should not duplicate it's title!")
        return

    def clean_summary(self):
        if len(self.cleaned_data.get('summary')) < 5:
            raise ValidationError(
                f"Значение должно быть длиннее 5 символов {self.cleaned_data.get('summary')} не подходит")
        return self.cleaned_data.get('summary')

    def clean_types(self):
        if not self.cleaned_data.get('types'):
            raise ValidationError("Выберите тип поста")
        return self.cleaned_data.get('types')

    def clean_stats(self):
        if not self.cleaned_data.get('stats'):
            raise ValidationError("Выберите статус поста")
        return self.cleaned_data.get('stats')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["users"]
        widgets = {
            "date_start": forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
            "date_end": forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'})
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('descriptions') == cleaned_data.get('name'):
            raise ValidationError("Text of the article should not duplicate it's title!")
        return

    def clean_name(self):
        if len(self.cleaned_data.get('name')) < 5:
            raise ValidationError(
                f"Значение должно быть длиннее 5 символов {self.cleaned_data.get('name')} не подходит")
        return self.cleaned_data.get('name')

class ProjectAddUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users')
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = users

    class Meta:
        model = Project
        exclude = ["name", "descriptions", "date_end", "date_start"]
        widgets = {
            "users": forms.CheckboxSelectMultiple,
            }