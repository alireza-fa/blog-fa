from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from .tasks import send_mail_task


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, verbose_name=_('username'), unique=True)
    email = models.EmailField(max_length=120, verbose_name=_('email'), unique=True)
    bio = models.CharField(max_length=250, verbose_name=_('bio'), null=True, blank=True)
    image = models.ImageField(verbose_name=_('image'), default='avatar.jpj')
    location = models.CharField(max_length=32, verbose_name=_('location'), null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_star = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin


class Follow(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')
    follow = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')

    def __str__(self):
        return f'{self.user} --> {self.follow}'
