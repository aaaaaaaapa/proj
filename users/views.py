from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from .forms import UserLoginForm, UserRegistrationForm
from posts.forms import Post


def login(request):

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, f'{username}, вы успешно вошли в аккаунт')
                return redirect('profile')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def registration(request):

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            user = form.instance
            auth.login(request, user)

            messages.success(request, f'{user.username}, вы успешно зарегистрировались и вошли в аккаунт')
            return redirect('profile')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile(request):

    page = request.GET.get('page', 1)
    query = request.GET.get('q', 'all')

    if query == 'draft':
        posts = Post.objects.filter(author_id=request.user.id, published_date__isnull=True).order_by('-created_date')
    else:
        posts = Post.objects.filter(author_id=request.user.id).order_by('-created_date')
    
    paginator = Paginator(posts, 4)
    current_page = paginator.page(int(page))


    return render(request, 'users/profile.html', {'posts': current_page})


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, f'Вы вышли из аккаунта')
    return redirect('login')

