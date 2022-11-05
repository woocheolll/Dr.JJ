from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.http import JsonResponse


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        profile = Profile()
        if form.is_valid():
            user = form.save()
            profile.user = user
            profile.save()
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    messages.warning(request, "로그아웃 되었습니다.")
    return redirect("accounts:index")


def index(request):
    users = get_user_model().objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/index.html", context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    messages.warning(request, "탈퇴되었습니다.")
    return redirect("accounts:index")


@login_required
def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/changepassword.html", context)


def detail(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)

    context = {"user": user}

    return render(request, "accounts/detail.html", context)


@login_required
# 새로운 프로필로 통합
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        if request.user == person:
            messages.warning(request, "스스로 팔로우를 할 수 없습니다.")
            return redirect("accounts:detail", user_pk)
            # if request.user.followings.filter(pk=user_pk).exists():
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True

        data = {
            "is_followed": is_followed,
            "following_cnt": person.followings.count(),
            "follower_cnt": person.followers.count(),
        }

        return JsonResponse(data)
    return redirect("accounts:login")


# 새로운 profile로 통합
# def profile(request, pk):
#     user = get_user_model().objects.get(pk=pk)
#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect("accounts:detail", pk)
#     else:
#         form = ProfileForm(instance=request.user.profile)
#     context = {
#         "user": user,
#         "form": form,
#     }
#     return render(request, "accounts/profile.html", context)


@login_required
def profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method == "POST":
        form1 = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        form2 = CustomUserChangeForm(request.POST, instance=request.user)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect("accounts:detail", pk)
        else:
            return render(request, "accounts/profile.html", context)
    else:
        form1 = ProfileForm(instance=request.user.profile)
        form2 = CustomUserChangeForm(instance=request.user)
    context = {
        "user": user,
        "form1": form1,
        "form2": form2,
    }
    return render(request, "accounts/profile.html", context)
