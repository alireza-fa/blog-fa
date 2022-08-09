from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.PostHomeView.as_view(), name='home'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/destroy/<int:post_id>/', views.PostDestroyView.as_view(), name='post_destroy'),
    path('explorer/', views.PostExplorerView.as_view()),
    path('post/detail/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),

    path('post/tag/create/', views.PostTagCreateView.as_view(), name='tag_create'),
    path('post/image/upload/', views.PostImageUploadView.as_view(), name='image_upload'),
    path('post/like/<int:post_id>/', views.PostLikeView.as_view(), name='post_like'),
    path('post/dislike/<int:post_id>/', views.PostDislikeView.as_view(), name='post_dislike'),
    path('post/save/<int:post_id>/', views.PostSaveView.as_view(), name='post_save'),
    path('post/comment/create/<int:post_id>/', views.PostCommentCreateView.as_view(), name='comment_create'),
    path('post/comment/destroy/<int:post_id>/<int:comment_id>/', views.PostCommentDestroyView.as_view()),
]
