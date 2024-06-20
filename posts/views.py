from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Post, Comment
from .forms import CommentForm, PostForm


def post_list(request):
    page = request.GET.get('page', 1)

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    paginator = Paginator(posts, 6)
    current_page = paginator.page(int(page))
    
    return render(request, 'posts/post_list.html', {'posts': current_page})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        comments = Comment.objects.filter(post_id=pk).order_by('-published_date')
    return render(request, 'posts/post_detail.html', {'post': post, 'form': form, 'comments': comments})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment_to_post.html', {'form': form})

# Create your views here.
