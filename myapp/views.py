from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,LoginForm,MessageForm,UsernameForm,EmailForm,IconForm
from .models import Talk
from django.contrib.auth.views import LoginView,PasswordChangeView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
User = get_user_model()
def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    error = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            for value in form.errors.values():
                if(error != '') : error += '\n'
                error += value
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form' : form,'error_message':error}) 

@login_required
def friends(request):
    friends = User.objects.exclude(id=request.user.id)
    users = []
    users_no_message = []
    users_have_message = []
    for friend in friends:
        message = Talk.objects.filter(Q(send_from=request.user.id,send_to=friend.id) | Q(send_from=friend.id,send_to=request.user.id)).order_by('date').last()
        if(message) : users_have_message.append({"id":friend.id,"icon":friend.icon,"username":friend.username,"date":message.date,"message":message.message})
        else : users_no_message.append({"id":friend.id ,"icon":friend.icon,"username":friend.username,"date":(friend.date_joined),"message":None})
    users_have_message = sorted(users_have_message,key=lambda x:x["date"],reverse=True)
    users_no_message = sorted(users_no_message,key=lambda x:x["date"],reverse=True)
    for user in users_have_message:
        users.append(user)
    for user in users_no_message:
        users.append(user)
    return render(request, "myapp/friends.html", {'users' : users})

@login_required
def talk_room(request,pk):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if(form.is_valid()):
            talk = form.save(commit=False)
            talk.send_from = request.user.id
            talk.send_to = pk
            talk.save()
    form = MessageForm()
    talks = Talk.objects.filter(Q(send_from=request.user.id,send_to=pk) | Q(send_from=pk,send_to=request.user.id)).order_by("date")
    return render(request, "myapp/talk_room.html",{"form":form, "pk":pk,"user":{"to" : User.objects.get(id=pk).username,"from":request.user.username},"talks":talks})

@login_required
def setting(request):
    return render(request, "myapp/setting.html")
 
class Login(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"
    next_page = "friends"

@login_required 
def username_change(request):
    if(request.method == 'POST'):
        form = UsernameForm(request.POST,instance=request.user)
        if(form.is_valid()):
            form.save()
            return redirect('username_change_done')
    else:
        form = UsernameForm()
    return render(request, "myapp/username_change.html",{"form":form})

@login_required
def username_change_done(request):
    return render(request,"myapp/username_change_done.html")

@login_required
def email_change(request):
    if(request.method == 'POST'):
        form = EmailForm(request.POST,instance=request.user)
        if(form.is_valid()):
            form.save()
            return redirect('email_change_done')
    else:
        form = EmailForm()
    return render(request, "myapp/email_change.html",{"form":form})

@login_required
def email_change_done(request):
    return render(request,"myapp/email_change_done.html")

@login_required
def icon_change(request):
    if(request.method == 'POST'):
        form = IconForm(request.POST,request.FILES,instance=request.user)
        if(form.is_valid()):
            form.save()
            return redirect('icon_change_done')
    else:
        form = IconForm()
    return render(request, "myapp/icon_change.html",{"form":form})

@login_required
def icon_change_done(request):
    return render(request,"myapp/icon_change_done.html")

@login_required
def password_change(request):
    return render(request, "myapp/password_change.html")

@login_required
def password_change_done(request):
    return render(request,"myapp/password_change_done.html")

class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    template_name = "myapp/password_change.html"
    success_url = "password_change_done"

class Logout(LoginRequiredMixin,LogoutView):
    template_name = "myapp/index.html"
    next_page = "index"

