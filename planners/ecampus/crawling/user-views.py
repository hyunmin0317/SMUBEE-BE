from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from users.models import Profile

# 계정생성
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            profile = Profile(user=user, password=raw_password)
            profile.save()
            login(request, user)  # 로그인
            return redirect('home')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'users/signup.html', context)

