from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.mhome, name="mhome"),
    path('product1/', views.product1_view, name='product1'),  # Ensure this exists
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('sign-out/', views.logout_view, name='sign-out'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update-photo/', views.update_profile_photo, name='update_profile_photo'),
]