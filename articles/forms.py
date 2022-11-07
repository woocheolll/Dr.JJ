from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "addr",
            "position",
            "contact",
            "homepage",
            "menu",
            "image",
            "x",
            "y",
        ]
        widgets = {"menu": forms.Textarea(attrs={"rows": 1})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", "grade", "image")
