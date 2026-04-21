from django import forms

from clients.models import Client


class ClientForm(forms.ModelForm):
    """Форма для отображения нормального ввода с подсказками"""

    class Meta:
        model = Client
        fields = ["name", "email", "comment"]

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя"})

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email"})

        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})
