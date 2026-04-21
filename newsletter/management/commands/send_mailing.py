from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings
from newsletter.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = "Отправляет рассылку по ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылок")

    def handle(self, *args, **options):

        mailing_id = options["mailing_id"]

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Рассылка с ID {mailing_id} не найдена"))
            return

        mailing.update_status()

        if mailing.status != "started":
            self.stdout.write(self.style.WARNING("Рассылка не активна"))
            return

        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(mailing=mailing, status="successfully", server_response="OK")
            except Exception as e:
                MailingAttempt.objects.create(mailing=mailing, status="failed", server_response=str(e))
            self.stdout.write(self.style.SUCCESS(f"Рассылка {mailing_id} обработана"))
