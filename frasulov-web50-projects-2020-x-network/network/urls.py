
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.userinfo, name="profile"),
    path("following", views.following, name="following"),
    #api path

    path("following/posts", views.get_following_posts, name="followingPosts"),
    path("create", views.createPost, name="create"),
    path("profile/update/<str:post_id>", views.updateProfilePost, name="update1"),
    path("update/<str:post_id>", views.updatePost, name="update"),
    path("posts", views.get_posts, name="posts"),
    path("like/<str:post_id>", views.like, name="like"),
    path("profile/<str:username>/posts", views.get_profile_posts, name="profilepost"),
    path("profile/like/<str:post_id>", views.profile_like, name="profileike"),
    path("profile/follow/<str:username>", views.follow, name="follow"),
]
