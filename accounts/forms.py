from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from accounts.models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()

        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "status_message"]
        labels = {
            "image": "프로필 이미지",
            "status_message": "상태메시지",
        }
