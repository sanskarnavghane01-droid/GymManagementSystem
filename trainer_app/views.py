from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import TrainerForm
from .models import Trainer


# Admins are redirected to the built-in Django admin site; no separate admin dashboard view.

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



# Create your views here.



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

