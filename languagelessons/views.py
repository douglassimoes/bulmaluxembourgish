from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from languagelessons import models

# Create your views here.

def home(request):
    if request.method == 'POST':
        print(request.POST.keys())
        if request.POST.get("login"):
            redirect('login')
        else:
            redirect('signup')
    return render(request,"languagelessons/home.html",{})

def signup(request):
    if request.method == 'POST':
        print(request.POST.keys())
        form = UserCreationForm(request.POST)
        dir(form.data)
        for field in form:
            print("Field Error {} {}".format(field.name, field.errors))
        if form.is_valid():
            user = form.save()
            post = request.POST
            print("Form valid")
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')    
    return render(request,"languagelessons/signup.html",{})

def login_view(request):
    if request.method == 'POST':
        print(request.POST.keys())
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request,"languagelessons/login.html",{})

@login_required
def dashboard(request):
    return render(request, 'languagelessons/dashboard.html',{"user_id": request.user.pk})

@login_required
def importlesson(request):
    return render(request,"languagelessons/importlesson.html",{})

# @login_required
def lesson(request):
    return render(request,"languagelessons/lesson.html",{})
