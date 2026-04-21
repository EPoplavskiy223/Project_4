from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from config import settings
from newsletter.forms import MailingForm, NewsletterForm
from newsletter.models import Mailing, MailingAttempt, Message


class MessageListView(ListView):
    model = Message
    template_name = "newsletter/message_list.html"
    context_object_name = "message_list"

class MessageDetailView(DetailView):
    model = Message
    template_name = "newsletter/message_detail.html"
    context_object_name = "message"

class MessageCreateView(CreateView):
    model = Message
    form_class = NewsletterForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")

class MessageUpdateView(UpdateView):
    model = Message
    form_class = NewsletterForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")

class MessageDeleteView(DeleteView):
    model = Message
    template_name = "newsletter/message_delete.html"
    success_url = reverse_lazy("newsletter:message_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "newsletter/mailing_list.html"
    context_object_name = "mailing_list"

class MailingDetailView(DetailView):
    model = Mailing
    template_name = "newsletter/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "newsletter/mailing_delete.html"
    success_url = reverse_lazy("newsletter:mailing_list")


class MailingSendView(View):
    """Запуск рассылки по кнопке"""

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.update_status()

        if mailing.status != "started":
            messages.error(request, "Рассылка не активна в данный момент")
            return redirect("newsletter:mailing_detail", pk=pk)

        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="successfully",
                    server_response="OK",
                )

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="failed",
                    server_response=str(e),
                )

        messages.success(request, f"Рассылка #{pk} обработана")
        return redirect("newsletter:mailing_detail", pk=pk)


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "newsletter/mailing_attempt_list.html"
    context_object_name = "attempts"
    ordering = ["attempt_time"]
