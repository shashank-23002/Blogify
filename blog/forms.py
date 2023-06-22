from django import forms
from .models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        exclude=["post"]
        labels={
            "user_name":"Your name",
            "email": "Your Email",
            "body" : "Your comment"
        }