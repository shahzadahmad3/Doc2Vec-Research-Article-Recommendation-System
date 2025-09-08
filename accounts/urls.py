from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path("login/", views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]