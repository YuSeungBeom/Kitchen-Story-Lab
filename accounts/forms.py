from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=50, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'nickname', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'nickname', 'profile_image', 'bio')