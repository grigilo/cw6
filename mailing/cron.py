import smtplib
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
from config import settings
from mailing.models import MailingSettings, MailingStatus


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = MailingSettings.objects.filter(
        first_datetime__lte=current_datetime).filter(
        setting_status__in=['Create'])

    for mailing in mailings:
        title = mailing.message.title
        content = mailing.message.content
        mailing.setting_status = 'Started'
        mailing.save()
        try:
            server_response = send_mail(
                subject=title,
                message=content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.email for recipient in
                                mailing.recipients.all()],
                fail_silently=False,
            )
            if server_response == 1:
                server_response = 'Письмо успешно отправлено'
                MailingStatus.objects.create(status='success',
                                             mailing_response=server_response,
                                             mailing_list=mailing)
            mailing.setting_status = 'Create'

            if mailing.sending == 'daily' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='dayly')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(
                    days=1)
                mailing.setting_status = 'Create'


            elif mailing.sending == 'weekly' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='weekly')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(
                    days=7)
                mailing.setting_status = 'Create'

            elif mailing.sending == 'monthly' and server_response == 1:
                current_datetime = MailingSettings.objects.get(
                    sending='monthly')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(
                    days=30)
                mailing.setting_status = 'Create'

            mailing.save()

        except smtplib.SMTPException as error:
            MailingStatus.objects.create(status='fail', mailing_response=error,
                                         mailing_list=mailing)


