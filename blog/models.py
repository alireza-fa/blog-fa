from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .managers import IsActiveManager


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', verbose_name=_('user'))
    title = models.CharField(max_length=120, verbose_name=_('title'))
    body = models.TextField(verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f'{self.user}-{self.title[:32]}'


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name=_('post'))
    image = models.ImageField(verbose_name=_('image'))

    class Meta:
        verbose_name = _('Post Image')
        verbose_name_plural = _('Post Images')

    def __str__(self):
        return f'{self.pk}-{self.post.title[:32]}'


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags', verbose_name=_('post'))
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return f'{self.pk}-{self.post.title[:32]}'


class PostComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comment', verbose_name=_('user'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('post'))
    body = models.CharField(max_length=512, verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Post Comment')
        verbose_name_plural = _('Post Comments')

    def __str__(self):
        return f'{self.user}-{self.post.title[:32]}'


class PostLike(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.CASCADE, verbose_name=_('user'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name=_('post'))

    class Meta:
        verbose_name = _('Post Like')
        verbose_name_plural = _('Post Likes')

    def __str__(self):
        return f'{self.user}-{self.post.title[:32]}'


class PostDislike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dislikes', verbose_name=_('user'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes', verbose_name=_('post'))

    class Meta:
        verbose_name = _('Post Dislike')
        verbose_name_plural = _('Post Dislikes')

    def __str__(self):
        return f'{self.user}-{self.post.title[:32]}'


class PostSave(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=_('saves'), verbose_name=_('user'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves', verbose_name=_('post'))

    class Meta:
        verbose_name = _('Post Save')
        verbose_name_plural = _('Post Saves')

    def __str__(self):
        return f'{self.user}-{self.post.title}'
