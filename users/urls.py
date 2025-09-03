from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/accounts/profile/'
    ), name='password_change'),
    path('profile/update/', views.update_profile_field, name='update_profile_field'),
    path('profile/upload-avatar/', views.upload_avatar, name='upload_avatar'),
]