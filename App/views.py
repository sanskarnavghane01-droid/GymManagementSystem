from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages

from .models import Member
from App.models import MembershipPlan

from django.db.models import Q
from datetime import date


def home(request):
    return render(request, 'index.html')


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
                user = authenticate(
                    request, username=username, password=password)
            except User.DoesNotExist:
                # Fall back to username/member id
                user = authenticate(
                    request, username=identifier, password=password)
            except User.MultipleObjectsReturned:
                # If multiple users share the same email, prefer the first match
                user_obj = User.objects.filter(
                    email__iexact=identifier).first()
                if user_obj:
                    user = authenticate(
                        request, username=user_obj.get_username(), password=password)

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
            messages.error(
                request, 'You do not have permission to access that page.')
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
    messages.error(
        request, 'You do not have permission to access the member dashboard.')
    return redirect('login')


@login_required
def add_member(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        membership_plan = MembershipPlan.objects.get(
            id=request.POST.get("membership_plan"))
        joining_date = request.POST.get("joining_date")
        expiry_date = request.POST.get("expiry_date")

        status = "Active"

        if date.fromisoformat(expiry_date) < date.today():
            status = "Expired"

        Member.objects.create(
            name=name,
            email=email,
            phone=phone,
            age=age,
            gender=gender,
            membership_plan=membership_plan,
            joining_date=joining_date,
            expiry_date=expiry_date,
            membership_status=status
        )

        return redirect("view_members")

    plans = MembershipPlan.objects.all()
    return render(request, "add_member.html", {"plans": plans})


@login_required
def view_members(request):

    members = Member.objects.all()

    search = request.GET.get("search")

    if search:
        members = members.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    status = request.GET.get("status")

    if status:
        members = members.filter(membership_status=status)

    return render(request, "view_members.html", {
        "members": members
    })


@login_required
def edit_member(request, id):

    member = Member.objects.get(id=id)

    if request.method == "POST":

        member.name = request.POST.get("name")
        member.email = request.POST.get("email")
        member.phone = request.POST.get("phone")
        member.age = request.POST.get("age")
        member.gender = request.POST.get("gender")
        member.membership_plan = MembershipPlan.objects.get(
            id=request.POST.get("membership_plan"))
        member.joining_date = request.POST.get("joining_date")
        member.expiry_date = request.POST.get("expiry_date")

        if member.expiry_date < date.today():
            member.membership_status = "Expired"
        else:
            member.membership_status = "Active"

        member.save()

        return redirect("view_members")

    plans = MembershipPlan.objects.all()

    return render(request, "edit_member.html", {
        "member": member,
        "plans": plans
    })


@login_required
def delete_member(request, id):

    member = Member.objects.get(id=id)

    member.delete()

    return redirect("view_members")


@login_required
def member_profile(request, id):

    member = Member.objects.get(id=id)

    return render(request, "member_profile.html", {
        "member": member
    })


@login_required
def member_stats(request):

    total = Member.objects.count()

    active = Member.objects.filter(
        membership_status="Active"
    ).count()

    expired = Member.objects.filter(
        membership_status="Expired"
    ).count()

    return render(request, "member_stats.html", {
        "total": total,
        "active": active,
        "expired": expired
    })
