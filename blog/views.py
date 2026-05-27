from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Post,Comment

from .forms import PostForm,CommentForm
from rest_framework.decorators import api_view

from rest_framework.response import Response

from .serializers import PostSerializer, CommentSerializer


def home_view(request):

    posts = Post.objects.all().order_by('-created_at')

    comment_form = CommentForm()

    return render(request, 'blog/home.html', {

        'posts': posts,

        'comment_form': comment_form
    })


@login_required
def create_post(request):

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.user = request.user

            post.save()

            return redirect('home')

    else:

        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def update_post(request, post_id):

    post = Post.objects.get(id=post_id)

    if post.user != request.user:

        return redirect('home')

    if request.method == 'POST':

        form = PostForm(request.POST, instance=post)

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = PostForm(instance=post)

    return render(request, 'blog/update_post.html', {'form': form})

@login_required
def delete_post(request, post_id):

    post = Post.objects.get(id=post_id)

    if post.user == request.user:

        post.delete()

    return redirect('home')

@login_required
def add_comment(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.user = request.user

            comment.post = post

            comment.save()

    return redirect('home')

@api_view(['GET'])
def posts_api(request):

    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def comments_api(request):

    comments = Comment.objects.all()

    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data)