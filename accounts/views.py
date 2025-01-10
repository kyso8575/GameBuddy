from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from .forms import SignupForm
from .models import Users

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method=="POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, form.get_user())
            next_url = request.GET.get("next") or "index"
            return redirect("common:home")
    else:
        form = AuthenticationForm()
    context = {"form":form}
    return render(request, "accounts/login.html", context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("common:home")

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            nickname = form.cleaned_data.get('nickname')
            age = form.cleaned_data.get('age')
            gender = form.cleaned_data.get('gender')
            preference1 = form.cleaned_data.get('preference1')
            preference2 = form.cleaned_data.get('preference2')
            user = authenticate(username=username, password=raw_password)
            login(request, user)  # 로그인
            return redirect('signup_complete')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def signup_complete(request):
    return render(request, 'accounts/signup_complete.html')

def check_username(request):
    username = request.GET.get('username', None)
    exists = Users.objects.filter(username=username).exists()  #아이디랑 닉네임 중복체크기능(구현중)
    return JsonResponse({'exists': exists})

def check_nickname(request):
    nickname = request.GET.get('nickname', None)
    exists = Users.objects.filter(nickname=nickname).exists()
    return JsonResponse({'exists': exists})