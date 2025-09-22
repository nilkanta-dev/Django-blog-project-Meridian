
from django.urls import path
from core.views import (PostListView, PostDetailView,single_user_posts,edit_comment,
    delete_comment,reply_comment,CommentVoteView)


urlpatterns = [
    
    path('',PostListView.as_view(),name='post-lists'),
    path('post/<slug:slug>/',PostDetailView.as_view(),name='post-detail'),
    path('post/<slug:slug>/comments/<int:comment_pk>/edit_comment/',edit_comment,name='edit_comment'),
    path('post/<slug:slug>/comments/<int:comment_pk>/delete_comment',delete_comment,name='delete_comment'),
    path('post/<slug:slug>/comments/<int:comment_pk>/reply/', reply_comment, name='reply_comment'),
    path('post/<slug:slug>/comments/<int:comment_pk>/vote/<slug:value>/',CommentVoteView.as_view(),name="comment_vote"),
    path('author/<str:username>/',single_user_posts,name='single_user_posts'),


]