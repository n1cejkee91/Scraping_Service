from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

User = get_user_model()

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                user.city = form.cleaned_data['city']
                user.language = form.cleaned_data['language']
                user.send_email = form.cleaned_data['send_email']
                user.save()
                return redirect('accounts:update')
        else:
            form = UserUpdateForm(initial={'city': user.city, 'language': user.language, 'send_email': user.send_email})
            return render(request, 'accounts/update.html', {'form': form})

    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            user = User.objects.get(pk=user.pk)
            user.delete()
    return redirect('home')