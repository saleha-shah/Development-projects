from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout

from app1.forms import RegisterForm, LoginForm, EditProfileForm, UserEditForm
from app1.models import ProfileInfo


@login_required
def profile(request):
    user_profile = ProfileInfo.objects.get(user=request.user)
    return render(request, 'app1/profile.html', {'user_profile': user_profile})


def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'app1/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            profile = ProfileInfo(
                user=user,
                gender=form.cleaned_data['gender'],
                dob=form.cleaned_data['dob']
                )
            profile.save()

            messages.success(request, 'You have signed up successfully.')
            login(request, user)

            return redirect('profile')
        else:
            messages.error(request, 'Invalid signup')
            return render(request, 'app1/register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'app1/signin.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')

                return redirect('profile')

        messages.error(request, 'Invalid username or password')

        return render(request, 'app1/signin.html', {'form': form})


def user_list(request):
    users = User.objects.all()
    return render(request, 'app1/user_list.html', {'users': users})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()

    return redirect('user_list')


@login_required
def sign_out(request):
    logout(request)
    return redirect('signin')


@login_required
def edit_profile(request):
    user = request.user
    profile = ProfileInfo.objects.get(user=user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'app1/edit_profile.html', context)
