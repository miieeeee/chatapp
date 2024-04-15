from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change',views.username_change,name='username_change'),
    path('icon_change',views.icon_change,name='icon_change'),
    path('username_change_done',views.username_change_done,name='username_change_done'),
    path('icon_change_done',views.icon_change_done,name='icon_change_done'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('password_change',views.PasswordChange.as_view(),name='password_change'),
    path('password_change_done',views.password_change_done,name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]