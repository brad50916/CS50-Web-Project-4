from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.post_like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("<str:id>", views.profile, name="profile")
]
