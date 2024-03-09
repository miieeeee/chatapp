from django import forms
from django.contrib.auth import get_user_model
from .models import Talk
from allauth.account.forms import SignupForm

User = get_user_model()


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
class IconForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["icon"]
        labels = {"icon":"New Icon"}

class MyCustomSignupForm(SignupForm):
    icon = forms.ImageField()
    class Meta:
        model = User

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        # Add your own processing here.
        # You must return the original result.
        user.icon = self.cleaned_data['icon']
        user.save()
        return user
    
class FriendSearchForm(forms.Form):
    search_name = forms.CharField(max_length=50,required=False)
    search_name.widget.attrs.update({'class':'search-box'})