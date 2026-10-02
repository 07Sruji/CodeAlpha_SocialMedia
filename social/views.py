from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CommentForm,
    PostForm,
    ProfileForm,
    RegisterForm,
    UserForm,
)

from .models import (
    Bookmark,
    Like,
    PollOption,
    PollVote,
    Post,
    Profile,
    Follow,
)


# =========================================================
# PROFILE HELPER
# =========================================================

def profile_for(user):
    return Profile.objects.get_or_create(user=user)[0]


# =========================================================
# HOME
# =========================================================

@login_required
def home(request):

    posts = (
        Post.objects
        .select_related("user")
        .prefetch_related(
            "comments__user",
            "likes",
            "bookmarks",
            "poll_options__votes",
        )
    )

    liked = set(
        Like.objects
        .filter(
            user=request.user,
            post__in=posts
        )
        .values_list("post_id", flat=True)
    )

    saved = set(
        Bookmark.objects
        .filter(
            user=request.user,
            post__in=posts
        )
        .values_list("post_id", flat=True)
    )

    return render(
        request,
        "social/home.html",
        {
            "posts": posts,
            "post_form": PostForm(),
            "liked": liked,
            "saved": saved,
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        user = form.save()

        profile_for(user)

        login(request, user)

        return redirect("home")

    return render(
        request,
        "social/register.html",
        {
            "form": form
        }
    )


# =========================================================
# CREATE POST
# =========================================================

@login_required
def create_post(request):

    if request.method != "POST":
        return redirect("home")

    form = PostForm(
        request.POST,
        request.FILES
    )

    if form.is_valid():

        post = form.save(commit=False)

        post.user = request.user

        post.save()

        # Poll options
        if post.post_type == "poll":

            options = [
                x.strip()
                for x in form.cleaned_data["poll_options"].splitlines()
                if x.strip()
            ]

            for option in options:

                PollOption.objects.create(
                    post=post,
                    text=option
                )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# =========================================================
# DELETE POST
# =========================================================

# =========================================================
# DELETE POST
# =========================================================

@login_required
def delete_post(request, pk):

    post = get_object_or_404(
        Post,
        pk=pk
    )

    if request.method == "POST":

        post.delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# =========================================================
# LIKE / UNLIKE
# =========================================================

@login_required
def like(request, pk):

    post = get_object_or_404(
        Post,
        pk=pk
    )

    like_obj, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like_obj.delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# =========================================================
# BOOKMARK / UNSAVE
# =========================================================

@login_required
def bookmark(request, pk):

    post = get_object_or_404(
        Post,
        pk=pk
    )

    bookmark_obj, created = Bookmark.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        bookmark_obj.delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# =========================================================
# COMMENT
# =========================================================

@login_required
def comment(request, pk):

    post = get_object_or_404(
        Post,
        pk=pk
    )

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment_obj = form.save(
                commit=False
            )

            comment_obj.user = request.user
            comment_obj.post = post

            comment_obj.save()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# =========================================================
# FOLLOW / UNFOLLOW
# =========================================================

@login_required
def follow(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    if user != request.user:

        follow_obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user
        )

        if not created:
            follow_obj.delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# =========================================================
# PROFILE
# =========================================================

def profile(request, username):

    u = get_object_or_404(
        User,
        username=username
    )

    pr = profile_for(u)

    following = False

    if request.user.is_authenticated:

        following = Follow.objects.filter(
            follower=request.user,
            following=u
        ).exists()

    posts = (
        Post.objects
        .filter(user=u)
        .select_related("user")
        .prefetch_related(
            "likes",
            "comments__user"
        )
    )

    return render(
        request,
        "social/profile.html",
        {
            "profile_user": u,
            "profile": pr,
            "posts": posts,
            "following": following
        }
    )


# =========================================================
# EDIT PROFILE
# =========================================================

@login_required
def edit_profile(request):

    profile_obj = profile_for(
        request.user
    )

    user_form = UserForm(
        request.POST or None,
        instance=request.user
    )

    profile_form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile_obj
    )

    if (
        request.method == "POST"
        and user_form.is_valid()
        and profile_form.is_valid()
    ):

        user_form.save()
        profile_form.save()

        return redirect(
            "profile",
            request.user.username
        )

    return render(
        request,
        "social/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )


# =========================================================
# SAVED POSTS
# =========================================================

@login_required
def saved(request):

    posts = (
        Post.objects
        .filter(
            bookmarks__user=request.user
        )
        .distinct()
    )

    return render(
        request,
        "social/saved_posts.html",
        {
            "posts": posts
        }
    )


# =========================================================
# POLL VOTE
# =========================================================

@login_required
def vote(request, pk, option):

    post = get_object_or_404(
        Post,
        pk=pk,
        post_type="poll"
    )

    poll_option = get_object_or_404(
        PollOption,
        pk=option,
        post=post
    )

    # Remove previous vote
    PollVote.objects.filter(
        user=request.user,
        option__post=post
    ).delete()

    # Add new vote
    PollVote.objects.create(
        user=request.user,
        option=poll_option
    )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )