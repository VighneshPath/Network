
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("user/<str:user_name>", views.user, name = "user"),
    path("liked/<int:post_id>", views.liked),
    # path("unliked/<int:post_id>", views.unliked),
    # path("get_liked/<int:post_id>/<int:user_id>", views.get_liked),
    path("follow/<int:follower>/<int:following>", views.follow),
    path("edit_post", views.edit_post, name = "edit_post"),
]
