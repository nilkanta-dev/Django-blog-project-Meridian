from django.urls import path
from userprofiles.views import (
   signup_view, DashboardView,
   profile_view,edit_post,
   users_list,view_user_profile,
   delete_user,delete_post,create_post,publish_post)


from core.views import AllUsersPostListView
from .views import api_keys
from django.contrib.auth.views import LogoutView,LoginView
from .forms import SignInForm


urlpatterns = [

   path('signup/',signup_view,name='sign-up'),
   path('signin/',LoginView.as_view(template_name='userprofiles/signin.html',authentication_form=SignInForm),name='signin'),
   path('dashboard/',DashboardView.as_view(),name='dashboard'),
   path('signout/',LogoutView.as_view(next_page="/"),name='signout'),
   path('profile/',profile_view,name='profile_view'),
   path('dashboard/<int:post_id>/edit',edit_post,name='edit_post'),
   path('dashboard/users_list/',users_list,name='users_list'),
   path('dashboard/user_details/<int:pk>/delete',delete_user,name='delete_user'),
   path('dashboard/user_details/<int:pk>/',view_user_profile,name='view_user_profile'),
   path('dashboard/<int:post_id>/delete',delete_post,name='delete_post'),
   path('dashboard/create_post',create_post,name='create_post'),
   path('post/<slug:slug>/publish',publish_post,name='publish_post'),
   path('dashboard/all-users-post/',AllUsersPostListView.as_view(),name="all_users_post_list"),
   path('api-keys/',api_keys,name='api_keys')
]