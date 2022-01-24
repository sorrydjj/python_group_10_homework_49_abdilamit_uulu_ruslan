
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Type, Status, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = []
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