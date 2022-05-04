import re
from django.shortcuts import render, redirect
from .forms import PostForm, ProfileForm, RelationshipForm
from .models import Post, Comment, Like, Profile, Relationship
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

# When a URL request matches the pattern we just defined,
# Django looks for a function called index() in the views.py file.


def index(request):
    """The home page for Learning Log."""
    return render(request, "FeedApp/index.html")


@login_required
def profile(request):
    profile = Profile.objects.filter(
        user=request.user
    )  # user is one of the fields in profile model # get doesn't work with exist
    if not profile.exists():
        Profile.objects.create(user=request.user)
    profile = Profile.objects.get(user=request.user)

    if request.method != "POST":  # means method is get
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("FeedApp:profile")

    context = {"form": form}
    return render(request, "FeedApp/profile.html", context)


@login_required
def myfeed(request):
    comment_count_list = []
    like_count_list = []
    posts = Post.objects.filter(username=request.user).order_by("-date_posted")
    for p in posts:
        c_count = Comment.objects.filter(post=p).count()
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    zipped_list = zip(posts, comment_count_list, like_count_list)

    context = {"posts": posts, "zipped_list": zipped_list}
    return render(request, "FeedApp/myfeed.html", context)


@login_required
def new_post(request):
    if request.method != "POST":
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.username = request.user
            new_post.save()
            return redirect("FeedApp:myfeed")
    context = {"form": form}
    return render(request, "FeedApp/new_post.html", context)
