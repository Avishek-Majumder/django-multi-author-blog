import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import Http404, HttpResponseNotAllowed

from .models import Post, Category, Tag, Comment, Like, AuthorProfile
from .forms import UserRegisterForm, PostForm, CommentForm
from .decorators import author_required


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}! You are registered as a Reader. Please log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


@require_POST
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def home_view(request):
    post_list = Post.objects.filter(status=Post.PUBLISHED).select_related('category', 'author').prefetch_related('tags')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    })


def post_detail_view(request, slug):
    post = get_object_or_404(Post.objects.select_related('category', 'author').prefetch_related('tags'), slug=slug)

    # Draft visibility check: only author or superuser can view drafts
    if post.status == Post.DRAFT:
        if not request.user.is_authenticated or (request.user != post.author and not request.user.is_superuser):
            raise Http404("Post not found.")

    # Time-based session guard for view_count (cooldown of 900 seconds / 15 minutes)
    session_key = f'last_viewed_post_{post.pk}'
    last_viewed = request.session.get(session_key)
    current_time = time.time()
    
    if not last_viewed or (current_time - last_viewed > 900):
        Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        request.session[session_key] = current_time
        post.refresh_from_db()

    # Check if current user liked the post
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(post=post, user=request.user).exists()

    comments = post.comments.select_related('user').all()
    comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
    })


@login_required
@author_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save tags
            messages.success(request, f"Post '{post.title}' created successfully!")
            return redirect('author_dashboard')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create New Post'})


@login_required
@author_required
def post_edit_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Ownership check
    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit this post.")
        raise PermissionDenied("You cannot edit another author's post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f"Post '{post.title}' updated successfully!")
            return redirect('author_dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': f'Edit Post: {post.title}', 'post': post})


@login_required
@author_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Ownership check
    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete this post.")
        raise PermissionDenied("You cannot delete another author's post.")

    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f"Post '{title}' was deleted.")
        return redirect('author_dashboard')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
@author_required
def author_dashboard_view(request):
    # Retrieve only the logged-in author's posts (both Draft and Published)
    posts = Post.objects.filter(author=request.user).select_related('category').prefetch_related('likes', 'comments')
    
    total_posts = posts.count()
    published_count = posts.filter(status=Post.PUBLISHED).count()
    draft_count = posts.filter(status=Post.DRAFT).count()
    total_views = sum(p.view_count for p in posts)

    return render(request, 'blog/author_dashboard.html', {
        'posts': posts,
        'total_posts': total_posts,
        'published_count': published_count,
        'draft_count': draft_count,
        'total_views': total_views,
    })


def category_posts_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post_list = Post.objects.filter(category=category, status=Post.PUBLISHED).select_related('author')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category_posts.html', {
        'category': category,
        'page_obj': page_obj,
    })


def tag_posts_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post_list = Post.objects.filter(tags=tag, status=Post.PUBLISHED).select_related('category', 'author')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/tag_posts.html', {
        'tag': tag,
        'page_obj': page_obj,
    })


def search_view(request):
    query = request.GET.get('q', '').strip()
    post_list = Post.objects.filter(status=Post.PUBLISHED).select_related('category', 'author')

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/search_results.html', {
        'query': query,
        'page_obj': page_obj,
    })


def author_profile_view(request, username):
    author_user = get_object_or_404(User, username=username)
    # Only show published posts for public profiles
    post_list = Post.objects.filter(author=author_user, status=Post.PUBLISHED).select_related('category')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    profile = getattr(author_user, 'author_profile', None)

    return render(request, 'blog/author_profile.html', {
        'author_user': author_user,
        'profile': profile,
        'page_obj': page_obj,
        'total_published': post_list.count(),
    })


@login_required
@require_POST
def comment_create_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # Check if post is published or author/superuser viewing draft
    if post.status == Post.DRAFT and post.author != request.user and not request.user.is_superuser:
        raise Http404("Post not found.")

    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content'].strip()
        if content:
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Comment cannot be empty.")
    else:
        messages.error(request, "Failed to add comment.")

    return redirect('post_detail', slug=post.slug)


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment.objects.select_related('post', 'user'), pk=pk)

    # Permission check: comment author, post author, or site admin can delete
    can_delete = (
        request.user == comment.user or
        request.user == comment.post.author or
        request.user.is_superuser
    )

    if not can_delete:
        messages.error(request, "You are not authorized to delete this comment.")
        raise PermissionDenied("You cannot delete this comment.")

    if request.method == 'POST':
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('post_detail', slug=post_slug)

    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})


@login_required
@require_POST
def like_toggle_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    like_qs = Like.objects.filter(post=post, user=request.user)
    if like_qs.exists():
        like_qs.delete()
        messages.info(request, "You unliked this post.")
    else:
        Like.objects.create(post=post, user=request.user)
        messages.success(request, "You liked this post!")

    return redirect('post_detail', slug=post.slug)
