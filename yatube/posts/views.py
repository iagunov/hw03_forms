from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from .models import Group, Post
from .my_paginator import my_paginator_def
from .forms import PostForm


User = get_user_model()


def index(request):
    post_list = Post.objects.select_related().all()
    page_obj = my_paginator_def(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date')
    page_obj = my_paginator_def(post_list, request)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.filter(author=author.id)
    page_obj = my_paginator_def(post_list, request)
    context = {
        'author': author,
        'page_obj': page_obj,
        'number_post_list': post_list.count
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    num_posts = Post.objects.filter(author__username=post.author)
    context = {
        'post': post,
        'num_posts': num_posts.count
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    form = PostForm(request.POST or None)
    if request.user.username:
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return HttpResponseRedirect(f'/profile/{request.user.username}/')
        return render(request, 'posts/create_post.html', {'form': form})
    return HttpResponseRedirect('/auth/login/')
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(request.POST, instance=post)
    if post.author == request.user and request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/posts/{post_id}/')
        return render(request, 'posts/create_post.html',
                      {'form': form, 'is_edit': is_edit})
    if post.author == request.user:
        form = PostForm(instance=post)
        return render(request, 'posts/create_post.html', {'form': form})
    return HttpResponseRedirect(f'/posts/{post_id}/')
