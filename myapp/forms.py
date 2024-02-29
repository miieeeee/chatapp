from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Talk

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2','icon')
        labels = {'username':'Username', 'email':'Email address', 'password1':"Password", 'password2':'Password confirmation'}


class LoginForm(AuthenticationForm):
    pass

class MessageForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('message',)
        widgets = {"message":forms.TextInput()}

class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {"username":"New Username"}
class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        labels = {"email":"New Email"}
class IconForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["icon"]
        labels = {"icon":"New Icon"}