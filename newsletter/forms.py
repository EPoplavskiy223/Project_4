from django import forms
from django.forms import ModelForm
from django.utils import timezone

from newsletter.models import Mailing, Message


class NewsletterForm(ModelForm):
    """Форма для отображения нормального ввода с подсказками"""

    class Meta:
        model = Message
        fields = ["subject", "body"]

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему"})

        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите письмо"})


class MailingForm(ModelForm):
    """Форма проверки даты и вывода в нормальный инпут"""

    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipients"]

        widgets = {
            "start_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "message": forms.Select(attrs={"class": "form-control"}),
            "recipients": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def clean_start_time(self):
        """ Проверка начального времени"""
        start_time = self.cleaned_data.get('start_time')
        if start_time and start_time < timezone.now():
                raise forms.ValidationError('Дата не может быть в прошлом')
        return start_time

    def clean(self):
        """Проверка ---"""
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Дата начала должна быть раньше окончания")

        return cleaned_data
