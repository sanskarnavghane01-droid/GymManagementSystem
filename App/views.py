from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import TrainerForm
from .models import Trainer


def home(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        is_trainer = request.POST.get('is_trainer') == 'on'

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
                return redirect('member_dashboard')
            if user.groups.filter(name='Trainer').exists():
                return redirect('trainer_dashboard')

            messages.error(request, 'No member account exists for these credentials.')
            return redirect('login')
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

#trainer's view
@group_required('Trainer')
def trainer_list(request):
    query = request.GET.get('q', '').strip()
    trainers = Trainer.objects.all().order_by('full_name')

    if query:
        trainers = trainers.filter(
            full_name__icontains=query
        ) | trainers.filter(
            email__icontains=query
        ) | trainers.filter(
            specialization__icontains=query
        )

    return render(request, 'trainer_list.html', {'trainers': trainers, 'query': query})


@group_required('Trainer')
def trainer_detail(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    return render(request, 'trainer_detail.html', {'trainer': trainer})


@group_required('Trainer')
def trainer_create(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            trainer = form.save()
            messages.success(request, f'Trainer "{trainer.full_name}" added successfully.')
            return redirect('trainer_detail', pk=trainer.pk)
    else:
        form = TrainerForm()

    return render(request, 'trainer_form.html', {'form': form, 'title': 'Add Trainer'})


@group_required('Trainer')
def trainer_update(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)

    if request.method == 'POST':
        form = TrainerForm(request.POST, instance=trainer)
        if form.is_valid():
            trainer = form.save()
            messages.success(request, f'Trainer "{trainer.full_name}" updated successfully.')
            return redirect('trainer_detail', pk=trainer.pk)
    else:
        form = TrainerForm(instance=trainer)

    return render(request, 'trainer_form.html', {'form': form, 'title': 'Edit Trainer', 'trainer': trainer})


@group_required('Trainer')
def trainer_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)

    if request.method == 'POST':
        trainer_name = trainer.full_name
        trainer.delete()
        messages.success(request, f'Trainer "{trainer_name}" deleted successfully.')
        return redirect('trainer_list')

    return render(request, 'trainer_confirm_delete.html', {'trainer': trainer})

