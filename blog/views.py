from django.shortcuts import get_object_or_404
from .serializers import (PostSerializer, PostTagSerializer, PostImageSerializer, PostCommentSerializer,
                          PostLiteSerializer,)
from .models import Post, PostImage, PostTag, PostComment
from permissions import IsPostOwnerOrAdmin

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class PostCreateView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        Post.objects.create(user=request.user, **data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PostDestroyView(APIView):
    permission_classes = (IsPostOwnerOrAdmin,)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostExplorerView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostLiteSerializer
    queryset = Post.objects.all()


class PostHomeView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostLiteSerializer

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        following_list = self.request.user.following.all().values_list('user__id', flat=True)
        posts = Post.objects.filter(user__id__in=following_list)
        return posts


class PostDetailView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.serializer_class(instance=post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostUpdateView(APIView):
    permission_classes = (IsPostOwnerOrAdmin,)
    serializer_class = PostLiteSerializer

    def patch(self, request, post_id):
        obj = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, obj)
        serializer = self.serializer_class(data=request.data, instance=obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostTagCreateView(APIView):
    serializer_class = PostTagSerializer
    permission_classes = (IsPostOwnerOrAdmin,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = PostTag(**serializer.validated_data)
        self.check_object_permissions(request, obj.post)
        obj.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PostImageUploadView(APIView):
    serializer_class = PostImageSerializer
    permission_classes = (IsPostOwnerOrAdmin,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = PostImage(**serializer.validated_data)
        self.check_object_permissions(request, obj)
        obj.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        obj = get_object_or_404(Post, id=post_id)
        post_dislike = request.user.dislikes.filter(post=obj)
        if post_dislike.exists():
            post_dislike.delete()
        post_like = request.user.likes.filter(post=obj)
        if post_like.exists():
            post_like.delete()
        else:
            request.user.likes.create(post=obj)
        return Response(data={"msg": 'successfully'}, status=status.HTTP_200_OK)


class PostDislikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        obj = get_object_or_404(Post, id=post_id)
        post_like = request.user.likes.filter(post=obj)
        if post_like.exists():
            post_like.delete()
        post_dislike = request.user.dislikes.filter(post=obj)
        if post_dislike.exists():
            post_dislike.delete()
        else:
            request.user.dislikes.create(post=obj)
        return Response(data={"msg": 'successfully'}, status=status.HTTP_200_OK)


class PostSaveView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        obj = get_object_or_404(Post, id=post_id)
        post_save = request.user.saves.filter(post=obj)
        if post_save.exists():
            post_save.delete()
        else:
            request.user.saves.create(post=obj)
        return Response(data={"msg": 'successfully'}, status=status.HTTP_200_OK)


class PostCommentCreateView(APIView):
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        obj = get_object_or_404(Post, id=post_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        PostComment.objects.create(user=request.user, post=obj, body=serializer.validated_data['body'])
        return Response(data={"msg": 'comment created successfully.'})


class PostCommentDestroyView(APIView):
    permission_classes = (IsPostOwnerOrAdmin,)

    def delete(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        comment = get_object_or_404(post.comments.all(), id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
