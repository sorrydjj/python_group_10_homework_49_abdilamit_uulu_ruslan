from django.contrib.auth import get_user_model
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name="profile",
        verbose_name="Профиль",
        on_delete=models.CASCADE,
    )
    birth_date = models.DateField(
        null=True,
        blank=False,
        verbose_name="Дата рождения",
    )

    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="avatars/",
        null=True,
        blank=False
    )

    profile_link = models.CharField(max_length=1000,
                                    verbose_name="Ссылка на профиль",
                                    null=True,
                                    blank=True
                                    )

    profile_description = models.CharField(max_length=2000,
                                   verbose_name="Описание",
                                   null=True,
                                   blank=True
                                   )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return f"Профиль: {self.user.username}. {self.id}"