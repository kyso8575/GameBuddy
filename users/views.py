from django.shortcuts import render, redirect
from django.contrib import messages

def users(request):
    return render(request, "users/users.html")

def profile(request, username):
    context = {
        "username":username,
    }
    return render(request, "users/profile.html", context)

# def mypage(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, '로그인이 필요한 기능입니다.')
#         return redirect('/login/')
#     return render(request, 'mypage.html')