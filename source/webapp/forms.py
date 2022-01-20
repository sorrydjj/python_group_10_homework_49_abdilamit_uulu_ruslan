from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Type, Status, Task


# class TaskForm(forms.Form):
#     summary = forms.CharField(max_length=200, required=True, label="Название")
#     stats = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label="New", label="Статус")
#     types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(),  label="Тип",
#                                           widget=forms.CheckboxSelectMultiple,
#                                           required=True)
#     description = forms.CharField(max_length=2000, label="Описание",
#                               widget=widgets.Textarea(attrs={"rows": 5, "cols":50}))

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