from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    # =========================================================
    # LOGIN / LOGOUT
    # =========================================================

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="social/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    # =========================================================
    # HOME
    # =========================================================

    path(
        "",
        views.home,
        name="home",
    ),


    # =========================================================
    # REGISTER
    # =========================================================

    path(
        "register/",
        views.register_view,
        name="register",
    ),


    # =========================================================
    # POSTS
    # =========================================================

    path(
        "post/create/",
        views.create_post,
        name="create_post",
    ),

    path(
        "post/<int:pk>/delete/",
        views.delete_post,
        name="delete_post",
    ),

    path(
        "post/<int:pk>/like/",
        views.like,
        name="like",
    ),

    path(
        "post/<int:pk>/bookmark/",
        views.bookmark,
        name="bookmark",
    ),

    path(
        "post/<int:pk>/comment/",
        views.comment,
        name="comment",
    ),


    # =========================================================
    # PROFILE
    # =========================================================

    path(
        "user/<str:username>/",
        views.profile,
        name="profile",
    ),

    path(
        "user/<str:username>/follow/",
        views.follow,
        name="follow",
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile",
    ),


    # =========================================================
    # SAVED POSTS
    # =========================================================

    path(
        "saved/",
        views.saved,
        name="saved",
    ),


    # =========================================================
    # POLL
    # =========================================================

    path(
        "post/<int:pk>/vote/<int:option>/",
        views.vote,
        name="vote",
    ),

]