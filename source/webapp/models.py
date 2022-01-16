from django.db import models

# Create your models here.
class Task(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, default="Unknown", verbose_name="Заголовок")
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name="Описанние")
    stats = models.ForeignKey("webapp.Status",
                               on_delete=models.PROTECT,
                               related_name="status"
                               )
    types = models.ManyToManyField("webapp.Type",
                             related_name="types",
                             blank=True
                             )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"{self.pk} | summary: {self.summary}"

    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Status(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, default="New")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "status"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Type(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, default="Task")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"