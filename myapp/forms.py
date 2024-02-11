from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    # img = forms.FileField()
    username = forms.CharField(label='Username',help_text='')
    email = forms.EmailField(label="Email address", required=True)
    password1 = forms.CharField(    
                                    label=("Password"),
                                    widget=forms.PasswordInput,
                                    help_text=''
                                )
    password2 = forms.CharField(
                                    label=("Password confirmation"),
                                    widget=forms.PasswordInput,
                                    help_text=("")
                                )
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2','icon')


class LoginForm(AuthenticationForm):
    pass

class MessageForm(forms.Form):
    message = forms.CharField(
        label="message",
        max_length=1000,
        required=True,
        widget=forms.TextInput()
    )


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