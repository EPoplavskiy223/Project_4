from django.db import models


class Client(models.Model):
    """Модель получателя рассылки"""

    name = models.CharField(max_length=255, verbose_name="Ф.И.О.")
    email = models.EmailField(unique=True, null=False, blank=False, verbose_name="Email")

    comment = models.TextField(verbose_name="Комментарий", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.name} <<< {self.email} >>>"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
