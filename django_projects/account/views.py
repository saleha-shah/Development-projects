import json

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator

from account.forms import RegisterForm, LoginForm, EditProfileForm, UserEditForm
from account.models import ProfileInfo, Listing


def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required
def profile(request):
    user_profile = ProfileInfo.objects.get(user=request.user)
    return render(request, 'account/profile.html', {'user_profile': user_profile})


def signup(request):
    if request.method == 'GET':
        return render(request, 'account/register.html', {'form': RegisterForm()})

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

            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid signup')
            return render(request, 'account/register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'account/signin.html', {'form': LoginForm()})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {user.first_name} {user.last_name}, welcome back!')

                return redirect('dashboard')

        messages.error(request, 'Invalid username or password')

        return render(request, 'account/signin.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    return redirect('dashboard')


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
            messages.success(request, 'Changes saved successfully!')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

    return render(request, 'account/edit_profile.html', {'forms': [user_form, profile_form]})


def decode_json(object):
    return json.decoder.JSONDecoder().decode(object)


def listing_page(request):
    products = Listing.objects.all()

    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    listings = []
    for listing in pages:
        image_url = decode_json(listing.image_urls)[0]
        listings.append({
            'listing': listing,
            'image_url': image_url
        })

    return render(request, 'account/listings.html', {'listings': listings, 'pages': pages})


def product_detail(request, product_id):
    product = Listing.objects.get(id=product_id)

    image_urls = decode_json(product.image_urls)
    description = decode_json(product.description)

    data = {
        'product': product,
        'image_urls': image_urls,
        'description': description,
    }
    
    return render(request, 'account/product_detail.html', data)
