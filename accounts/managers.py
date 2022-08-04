from django.contrib.auth.models import BaseUserManager
from random import randint


class UserManager(BaseUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def create_user(self, username, email, password):
        if not username:
            username = str(randint(1000000000, 99999999999))
        if not email:
            raise ValueError('User must have email')
        user = self.model(username=username)
        user.email = BaseUserManager.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
