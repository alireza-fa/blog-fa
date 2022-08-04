from django.core.cache import cache
from random import randint
from accounts.tasks import send_mail_task
from django.utils.translation import gettext_lazy as _


def send_otp_code(email, username, password):
    run = 1
    while run:
        code = randint(1000, 9999)
        if not cache.get(key=code):
            run = 0
    cache.set(key=str(code), value={"email": email, "username": username, "password": password}, timeout=120)
    send_mail_task.delay(email, _('otp code'), str(code))


def send_otp_code_forget_password(email):
    run = 1
    while run:
        code = randint(10000, 99999)
        if not cache.get(key=code):
            run = 0
    cache.set(key=str(code), value={"email": email}, timeout=120)
    send_mail_task.delay(email, _('otp code for forget password'), str(code))


def check_otp_code(code):
    info = cache.get(key=code)
    if info:
        return info
    return False
