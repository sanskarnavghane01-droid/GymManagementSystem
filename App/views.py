from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import Member


def home(request):
    return render(request, 'index.html')

def member_list(request):
    members = Member.objects.all()

    return render(request,'members.html',
                  {
                      "members":members
                  }
            )


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

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
            # Redirect based on group membership
            if user.groups.filter(name='Admin').exists() or user.is_superuser:
                return redirect('/admin/')
            if user.groups.filter(name='Trainer').exists():
                return redirect('trainer_dashboard')
            # Default to member dashboard for all other authenticated users
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access that page.')
            return redirect('login')

        return _wrapped

    return decorator


# Admins are redirected to the built-in Django admin site; no separate admin dashboard view.


@group_required('Trainer')
def trainer_dashboard(request):
    return render(request, 'trainer_dashboard.html')


@login_required
def member_dashboard(request):
    # Members are allowed only if they are in Member group or not staff
    user = request.user
    if user.is_superuser or user.groups.filter(name='Member').exists() or not user.is_staff:
        return render(request, 'member_dashboard.html')
    messages.error(request, 'You do not have permission to access the member dashboard.')
    return redirect('login')

