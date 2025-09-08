from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()   # ✅ works with custom user model
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")   # ✅ safe
        password = request.POST.get("password")
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next") or "home")
            else:
                messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('home')
