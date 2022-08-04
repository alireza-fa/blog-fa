from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_task(email, subject, message):
    send_mail(from_email='alirezafeyze44@gmail.com', subject=subject, message=message, recipient_list=[email])
    return True
