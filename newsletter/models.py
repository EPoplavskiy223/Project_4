from django.db import models
from django.utils import timezone


class Message(models.Model):
    """Модель сообщения рассылки"""

    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"


class Mailing(models.Model):
    """Модель Статуса рассылки"""

    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время конца")

    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    message = models.ForeignKey("Message", on_delete=models.PROTECT, verbose_name="Письмо")

    recipients = models.ManyToManyField("clients.Client", related_name="recipients", verbose_name="Получатели")

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус",
    )

    def update_status(self):
        """Динамическое изменение статуса рассылки"""
        now = timezone.now()

        if now < self.start_time:
            new_status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            new_status = self.STATUS_STARTED
        else:
            new_status = self.STATUS_FINISHED

        if new_status != self.status:
            self.status = new_status
            self.save(update_fields=["status"])

    def __str__(self):
        return f"Рассылка: {self.pk} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingAttempt(models.Model):
    """Попытка отправки письма (ЛОГИ)"""

    STATUS_SUCCESSFULLY = "successfully"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [(STATUS_SUCCESSFULLY, "Успешно"), (STATUS_FAILED, "Не успешно")]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    server_response = models.TextField(blank=True)
    mailing = models.ForeignKey("Mailing", on_delete=models.CASCADE, verbose_name="Рассылка")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_FAILED,
        verbose_name="Статус",
    )
