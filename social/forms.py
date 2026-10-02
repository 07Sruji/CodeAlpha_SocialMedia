from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment,Post,Profile
class RegisterForm(UserCreationForm):
 email=forms.EmailField(required=True)
 class Meta: model=User; fields=["username","email","password1","password2"]
class PostForm(forms.ModelForm):
 poll_options=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":3,"placeholder":"One poll option per line"}))
 class Meta:
  model=Post
  fields=["post_type","content","image","video","link_url","link_title","location_name","event_title","event_date","event_location"]
  widgets={"content":forms.Textarea(attrs={"rows":4,"placeholder":"Share your thoughts, ideas or something interesting..."}),"event_date":forms.DateTimeInput(attrs={"type":"datetime-local"})}
def clean(self):
    data = super().clean()

    post_type = data.get("post_type")
    content = (data.get("content") or "").strip()

    if post_type == "text" and not content:
        raise forms.ValidationError(
            "Please write something."
        )

    if post_type == "image" and not data.get("image"):
        raise forms.ValidationError(
            "Choose an image."
        )

    if post_type == "video" and not data.get("video"):
        raise forms.ValidationError(
            "Choose a video."
        )

    if post_type == "link" and not data.get("link_url"):
        raise forms.ValidationError(
            "Enter a link."
        )

    if post_type == "poll":
        options = [
            x.strip()
            for x in (data.get("poll_options") or "").splitlines()
            if x.strip()
        ]

        if len(options) < 2:
            raise forms.ValidationError(
                "Poll needs at least two options."
            )

    if post_type == "location" and not data.get("location_name"):
        raise forms.ValidationError(
            "Enter a location."
        )

    if post_type == "event" and not data.get("event_title"):
        raise forms.ValidationError(
            "Enter an event title."
        )

    return data
class CommentForm(forms.ModelForm):
 class Meta: model=Comment; fields=["content"]; widgets={"content":forms.TextInput(attrs={"placeholder":"Write a comment..."})}
class ProfileForm(forms.ModelForm):
 class Meta: model=Profile; fields=["bio","profile_image"]; widgets={"bio":forms.Textarea(attrs={"rows":4,"placeholder":"Tell people about yourself..."})}
class UserForm(forms.ModelForm):
 class Meta: model=User; fields=["first_name","last_name","email"]
