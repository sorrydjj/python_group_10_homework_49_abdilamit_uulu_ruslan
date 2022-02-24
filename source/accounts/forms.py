from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm

from accounts.models import Profile

User = get_user_model()

class MyUserCreationForm(UserCreationForm):
    email = forms.CharField(label="email", widget=forms.EmailInput, required=True)


    def clean(self):
        cleaned_data = super().clean()
        last_name = cleaned_data.get("last_name")
        first_name = cleaned_data.get("first_name")
        if not first_name:
            if not last_name:
                raise ValidationError("заполните хотя бы одно из полей: last_name, first_name")
        return cleaned_data

    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "birth_date", "profile_link", "profile_description")


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']