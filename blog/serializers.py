from rest_framework import serializers
from .models import Post, PostTag, PostImage, PostComment


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    count_like = serializers.SerializerMethodField(read_only=True)
    count_dislike = serializers.SerializerMethodField(read_only=True)
    count_save = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'created', 'modified', 'comments', 'images',
                  'tags', 'count_like', 'count_dislike', 'count_save')
        read_only_fields = ('user', 'id', 'created', 'modified')

    def get_comments(self, obj):
        comments = obj.comments.filter(is_active=True)
        return PostCommentSerializer(instance=comments, many=True).data

    def get_images(self, obj):
        images = obj.images.all()
        return PostImageSerializer(instance=images, many=True).data

    def get_tags(self, obj):
        tags = obj.tags.all()
        return PostTagSerializer(instance=tags, many=True).data

    def get_count_like(self, obj):
        return obj.likes.count()

    def get_count_dislike(self, obj):
        return obj.dislikes.count()

    def get_count_save(self, obj):
        return obj.saves.count()


class PostLiteSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    count_like = serializers.SerializerMethodField(read_only=True)
    count_dislike = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'created', 'modified', 'image',
                  'tags', 'count_like', 'count_dislike')
        read_only_fields = ('user', 'id', 'created', 'modified')

    def get_image(self, obj):
        image = obj.images.first()
        return PostImageSerializer(instance=image).data

    def get_tags(self, obj):
        tags = obj.tags.all()
        return PostTagSerializer(instance=tags, many=True).data

    def get_count_like(self, obj):
        return obj.likes.count()

    def get_count_dislike(self, obj):
        return obj.dislikes.count()

    def get_count_save(self, obj):
        return obj.saves.count()


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image')


class PostTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostTag
        fields = ('post', 'name')


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields = ('id', 'user', 'post', 'body', 'created', 'modified')
        read_only_fields = ('user', 'created', 'post', 'modified', 'id')
