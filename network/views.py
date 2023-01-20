import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Post, Profile, Like
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

class newpost(forms.Form):
    content = forms.CharField(label="",widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(newpost, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['style'] = 'width:700px; height:150px; display:block; border: 1px solid lightgray;'

def index(request):
    if request.method=="POST":
        if 'Post' in request.POST:
            form = newpost(request.POST)
            if form.is_valid():
                user=request.user
                content=form.cleaned_data["content"]
                new = Post(content=content, user=user, date = datetime.now())
                new.save()
                return HttpResponseRedirect(reverse("index"))
        # if 'Save' in request.POST:
        #     p = Post.objects.get(pk=request.POST.get("post_id"))
        #     p.content=request.POST.get("compose-body")
        #     p.save()
    posts = Post.objects.all().order_by("-date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list = [i for i in range(1,paginator.num_pages+1)]
    return render(request, "network/index.html", {
        "form" : newpost(),
        "empty" : Like.objects.none(),
        "page_obj": page_obj,
        "list": list
    })

def following(request):
    followed = Profile.objects.filter(user=request.user)
    post = Post.objects.none()
    for f in followed:
        post |= Post.objects.filter(user=f.following).order_by("-date")
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list = [i for i in range(1,paginator.num_pages+1)]
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "list": list
    })

def profile(request, id):
    user = User.objects.get(pk=id)
    post = Post.objects.filter(user=user).order_by("-date")
    count3 = Post.objects.filter(user=user)
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list = [i for i in range(1,paginator.num_pages+1)]

    following = Profile.objects.filter(user=user)
    follower = Profile.objects.filter(following=user)

    if request.user.is_authenticated == False:
        return render(request, "network/profile.html", {
            "user1" : user,
            "following" : following,
            "count1" : following.count(),
            "count2" : follower.count(),
            "count3" : count3.count(),
            "page_obj": page_obj,
            "list": list
        })
    else:
        if request.method == "POST":
            if 'unfollow' in request.POST:
                Profile.objects.get(user=request.user, following=user).delete()
            elif 'follow' in request.POST:
                add = Profile(user=request.user, following=user)
                add.save()
        try:
            Profile.objects.get(user=request.user, following=user)
            exist=1
        except Profile.DoesNotExist:
            exist=0

        me=0
        if request.user == user:
            me=1
        return render(request, "network/profile.html", {
            "user1" : user,
            "following" : following,
            "count1" : following.count(),
            "count2" : follower.count(),
            "count3" : count3.count(),
            "exist" : exist,
            "me" : me,
            "page_obj": page_obj,
            "list": list
        })

@csrf_exempt
@login_required
def post_like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            if data.get("like") == True:
                post.like += 1
                l = Like(user=request.user, post=post)
                l.save()
            elif data.get("like") == False:
                post.like -= 1
                Like.objects.get(user=request.user, post=post).delete()
            post.save()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def edit(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")
        p = Post.objects.get(pk=post_id)
        p.content=content
        p.save()
        return JsonResponse({"message": "Content sent successfully."}, status=201)
    
    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

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
