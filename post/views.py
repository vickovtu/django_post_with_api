from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages

from .forms import (
    PostCreateForm,
    UserLoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
    PostEditForm,
    CommentForm
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from post.models import Post, Profile, Comment


def post_list(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = Post.published.filter(
            Q(title__icontains=query) |
            Q(author__username=query) |
            Q(body__icontains=query)
        )

    paginator = Paginator(post_list, 5)  # создаем пагинатор
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  # берем указаную стр
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(posts, index=4)

    page_range = list(paginator.page_range)[start_index:end_index]

    context = {'post': posts, 'page_range': page_range}
    return render(request, "blog/post_list.html", context)


def proper_pagination(posts, index):
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number - index
        end_index = start_index + end_index
    return start_index, end_index


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_like = True if post.likes.filter(id=request.user.id).exists() \
        else False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(
                post=post,
                content=content,
                user=request.user,
                reply=comment_qs,
            )
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm
    context = {
        'post': post,
        'is_like': is_like,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,

    }
    return render(request, 'blog/post_detail.html', context)


def post_create(request):
    form = PostCreateForm
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post has been successful created .")
            return redirect('post_list')
        else:
            context = {
                'form': form,
                'error': 'not user'
            }
    return render(request, 'blog/post_create.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect(reverse('post_list'))
            else:
                return HttpResponse("user is not active")
        else:
            render(request, 'blog/login.html', {'form': form})
    else:
        form = UserLoginForm()
        context = {
            'form': form
        }
        return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('post_list')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('post_list')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        return render(
            request,
            'registration/register.html',
            {'form': UserRegistrationForm}
        )


@login_required
def edit_profile(request):
    form = ProfileEditForm
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None,
            instance=request.user.profile,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('post_list')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form

            }
            return render(request, 'blog/edit_profile.html', context)
    else:
        user_form = UserEditForm(instance=request.user)
        try:
            profile_form = ProfileEditForm(instance=request.user.profile)
        except User.profile.RelatedObjectDoesNotExist:
            Profile.objects.create(user=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form

        }
        return render(request, 'blog/edit_profile.html', context)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(post.get_absolute_url())


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog/post_edit.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    post.delete()
    messages.warning(request, "Post has been delete")
    return redirect('post_list')
