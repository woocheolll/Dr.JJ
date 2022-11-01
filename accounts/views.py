from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model


# Create your views here.

def detail(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)

