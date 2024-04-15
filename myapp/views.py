from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import MessageForm, UsernameForm, IconForm, FriendSearchForm
from .models import Talk
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q, OuterRef, Subquery

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")


@login_required
def friends(request):
    form = FriendSearchForm(request.GET)
    friends = User.objects.exclude(id=request.user.id)
    if form.is_valid():
        search_name = form.cleaned_data["search_name"]
        if search_name:
            friends = friends.filter(Q(username__contains=search_name) | Q(email__contains=search_name))
    users = []
    users_no_message = []
    users_have_message = []
    sub_qs = Talk.objects.filter(
        Q(send_from=request.user, send_to=OuterRef("id"))
        | Q(send_from=OuterRef("id"), send_to=request.user)
    ).order_by("-date")[:1]
    friends_with_message = friends.annotate(
        last_message=Subquery(sub_qs.values("message"))
    ).annotate(last_date=Subquery(sub_qs.values("date")))

    for friend in friends_with_message:
        if friend.last_message:
            users_have_message.append(
                {
                    "id": friend.id,
                    "icon": friend.icon,
                    "username": friend.username,
                    "date": friend.last_date,
                    "message": friend.last_message,
                }
            )
        else:
            users_no_message.append(
                {
                    "id": friend.id,
                    "icon": friend.icon,
                    "username": friend.username,
                    "date": (friend.date_joined),
                    "message": None,
                }
            )
    users_have_message = sorted(
        users_have_message, key=lambda x: x["date"], reverse=True
    )
    users_no_message = sorted(users_no_message, key=lambda x: x["date"], reverse=True)
    for user in users_have_message:
        users.append(user)
    for user in users_no_message:
        users.append(user)
    return render(request, "myapp/friends.html", {"users": users, "form": form})


@login_required
def talk_room(request, pk):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            talk = form.save(commit=False)
            talk.send_from = request.user
            talk.send_to = User.objects.get(id=pk)
            talk.save()
    form = MessageForm()
    talks = Talk.objects.filter(
        Q(send_from_id=request.user.id, send_to_id=pk)
        | Q(send_from_id=pk, send_to_id=request.user.id)
    ).order_by("date")
    return render(
        request,
        "myapp/talk_room.html",
        {
            "form": form,
            "pk": pk,
            "user": {
                "to": User.objects.get(id=pk).username,
                "from": request.user.username,
            },
            "talks": talks,
        },
    )


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


@login_required
def username_change(request):
    if request.method == "POST":
        form = UsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
    else:
        form = UsernameForm()
    return render(request, "myapp/username_change.html", {"form": form})


@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")


@login_required
def icon_change(request):
    if request.method == "POST":
        form = IconForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("icon_change_done")
    else:
        form = IconForm()
    return render(request, "myapp/icon_change.html", {"form": form})


@login_required
def icon_change_done(request):
    return render(request, "myapp/icon_change_done.html")


@login_required
def password_change_done(request):
    return render(request, "myapp/password_change_done.html")


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = "myapp/password_change.html"
    success_url = "password_change_done"


class Logout(LoginRequiredMixin, LogoutView):
    template_name = "myapp/index.html"
    next_page = "index"
