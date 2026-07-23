from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages



def home(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        is_trainer = request.POST.get('is_trainer') == 'on'
        next_url = request.POST.get('next', '').strip()

        if next_url and not next_url.startswith('/'):
            next_url = ''

        user = None
        # Try to find by email first
        if identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.get_username()
                user = authenticate(request, username=username, password=password)
            except User.DoesNotExist:
                # Fall back to username/member id
                user = authenticate(request, username=identifier, password=password)
            except User.MultipleObjectsReturned:
                # If multiple users share the same email, prefer the first match
                user_obj = User.objects.filter(email__iexact=identifier).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.get_username(), password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully signed in.')

            if is_trainer:
                if user.is_superuser or user.groups.filter(name='Trainer').exists():
                    return redirect('trainer_dashboard')
                messages.error(request, 'No trainer account exists for these credentials.')
                return redirect('login')

            if user.is_superuser or user.groups.filter(name='Admin').exists():
                return redirect('/admin/')
            if user.groups.filter(name='Member').exists() or not user.is_staff:
                if next_url:
                    return redirect(next_url)
                return redirect('member_dashboard')
            if user.groups.filter(name='Trainer').exists():
                return redirect('trainer_dashboard')

            messages.error(request, 'No member account exists for these credentials.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html', {'next_url': request.GET.get('next', '').strip()})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def member_dashboard(request):
    return render(request, 'member_dashboard.html')







