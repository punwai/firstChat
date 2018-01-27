from django.urls import path
from accounts.views import RegisterView, ProfileView
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns= [
    #punhub.net/accounts/login
    #pytpath('login/', LoginView, name='login'),
    #punhub.net/accounts/register
    path('register/', RegisterView.as_view() , name='register'),
    path('login/', auth_views.login, {'template_name':'accounts/login.html'},name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'} ,name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
 ]
