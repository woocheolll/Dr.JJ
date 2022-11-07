from django import forms
from .models import Freereview, Freecomment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Freereview
        fields = ["title", "content", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Freecomment
        fields = [
            "content",
        ]
        widgets = {"content": forms.Textarea(attrs={"rows": 1})}
