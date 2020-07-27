from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.core.paginator import Paginator
from django.views.generic import ListView

import datetime
import json

from .models import User, Post, Follow, Like

class ContactList(ListView):
    paginate_by = 2
    model = Post

def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        # When Submitting a new post, checking if the user is authenticated
        post = Post(user = request.user, content = request.POST["content"], time_stamp = datetime.datetime.utcnow())
        # Add Post to database
        post.save()

    posts = Post.objects.all().order_by('-time_stamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if(request.user.is_authenticated):
        liked_posts = Like.objects.filter(user = request.user)
        liked_posts_id = []
        for post in posts:
            for liked_post in liked_posts:
                if(post.id == liked_post.post.id):
                    liked_posts_id.append(post.id)
                    break
        return render(request, "network/index.html",
            {
                "posts":page_obj,
                "liked_posts": liked_posts_id
            }
        )
    return render(request, "network/index.html",
        {
            "posts":page_obj
        }
    )


def following(request):
    if request.method == "POST":
        post = Post(user = request.user, content = request.POST["content"], time_stamp = datetime.datetime.utcnow())
        # Add Post to database
        post.save()

    following_people = Follow.objects.filter(follower = request.user)
    following_posts = []
    posts = Post.objects.all().order_by('-time_stamp')
    for post in posts:
        for foll in following_people:
            if(post.user.id == foll.following.id):
                following_posts.append(post)
                break

    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_posts = Like.objects.filter(user = request.user)
    liked_posts_id = []
    for post in following_posts:
        for liked_post in liked_posts:
            if(post.id == liked_post.post.id):
                liked_posts_id.append(post.id)
                break
    return render(request, "network/following.html",
        {
            "posts":page_obj,
            "liked_posts": liked_posts_id
        }
    )



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def user(request, user_name):
    user_details = User.objects.filter(username = user_name).first()
    following = len(Follow.objects.filter(follower = user_details))
    followers = len(Follow.objects.filter(following = user_details))

    posts = Post.objects.filter(user = user_details).order_by('-time_stamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if(request.user.is_authenticated):
        liked_posts = Like.objects.filter(user = request.user)
        liked_posts_id = []
        for post in posts:
            for liked_post in liked_posts:
                if(post.id == liked_post.post.id):
                    liked_posts_id.append(post.id)
                    break
        if(len(Follow.objects.filter(follower = request.user, following = user_details)) != 0):
            current_state = True
        else:
            current_state = False
        return render(request, "network/user.html", {
            "user_details": user_details,
            "following": following,
            "followers": followers,
            "posts": page_obj,
            "liked_posts": liked_posts_id,
            "current_state": current_state
            })
    else:
        return render(request, "network/user.html", {
            "user_details": user_details,
            "following": following,
            "followers": followers,
            "posts": page_obj
            })

def liked(request, post_id):
    if(request.user.is_authenticated):
        try:
            post = Post.objects.get(pk = post_id)
            if(len(Like.objects.filter(user = request.user, post = post)) == 0):
                like = Like(user = request.user, post = post)
                post.likes+=1
                like.save()
                post.save()
            else:
                like = Like.objects.filter(user = request.user, post = post)
                post.likes-=1
                like.delete()
                post.save()

        except:
            pass
    return HttpResponse("")


# def unliked(request, post_id):
#     if(request.user.is_authenticated):
#         try:
#             post = Post.objects.get(pk=post_id)
#             like = Like.objects.filter(user = request.user, post = post)
#             if(len(like) != 0):
#                 post.likes-=1
#                 like.delete()
#                 post.save()
#         except:
#             pass

#     return HttpResponse("")

# def get_liked(request, post_id, user_id):
#     liked = Like.objects.filter(post = Post.objects.get(pk = post_id), user = User.objects.get(pk=user_id))
#     return HttpResponse(bool(liked))

def follow(request, follower, following):
    follower = User.objects.filter(id = follower).first()
    following = User.objects.filter(id = following).first()
    is_following = Follow.objects.filter(follower = follower, following = following)
    if(len(is_following) == 0):
        new_follow = Follow(follower = follower, following = following)
        new_follow.save()
    else:
        is_following.delete()

    return HttpResponse("")

def edit_post(request):
    # post = Post.objects.filter(id = post_id).first()
    # if(request.user == post.user):
    #     return render(request, "network/edit_post.html", {
    #             "post": post
    #         })

    # return render(request, "network/error.html", {
    #         "message" : "You do not have the permission to edit/modify this post!"
    #     })
    data = json.loads(request.body)
    post = Post.objects.filter(id =data["post_id"]).first()
    if(request.user == post.user):
        post.content = data["new_content"]
        post.save()
    return HttpResponse("")


