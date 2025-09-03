from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from shop.models import Order

@login_required(login_url="")
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', {'orders': orders})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


from django.http import JsonResponse
from .models import Profile

@login_required
def update_profile_field(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value')
        profile = request.user.profile

        if field in ['phone', 'address']:
            setattr(profile, field, value)
            profile.save()
            return JsonResponse({'status': 'ok', 'field': field, 'value': value})
        elif field == 'email':
            request.user.email = value
            request.user.save()
            return JsonResponse({'status': 'ok', 'field': field, 'value': value})
        return JsonResponse({'status': 'error', 'message': 'Невірне поле'})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
@csrf_exempt  # або використай csrf_token у JS
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = request.user.profile
        profile.avatar = request.FILES['avatar']
        profile.save()
        return JsonResponse({'status': 'ok', 'url': profile.avatar.url})
    return JsonResponse({'status': 'error'}, status=400)