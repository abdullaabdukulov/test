from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    # path('login/', views.user_login, name='login'),
    # path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='accounts:login',
    ), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('send/message/', views.MessageSendView.as_view(), name='sender'),
]