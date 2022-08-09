from django.contrib import admin
from .models import Post, PostImage, PostTag, PostComment, PostLike, PostDislike, PostSave


class PostImageInline(admin.TabularInline):
    model = PostImage


class PostTagInline(admin.TabularInline):
    model = PostTag


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('title', 'body', 'user__username')
    inlines = (PostImageInline, PostTagInline, )


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('user', )


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


@admin.register(PostDislike)
class PostDislikeAdmin(admin.ModelAdmin):
    list_display = ('user', )


@admin.register(PostSave)
class PostSaveAdmin(admin.ModelAdmin):
    list_display = ('user', )
