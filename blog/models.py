from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', verbose_name=_('user'))
    title = models.CharField(max_length=120, verbose_name=_('title'))
    body = models.TextField(verbose_name=_('body'))


class PostImage(models.Model):
    pass


class PostVideo(models.Model):
    pass


class Tag(models.Model):
    pass


class PostComment(models.Model):
    pass


class PostLike(models.Model):
    pass


class PostDislike(models.Model):
    pass


class PostSave(models.Model):
    pass
