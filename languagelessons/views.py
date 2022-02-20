from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.method == 'POST':
        print(request.POST.keys())
        if request.POST.get("login"):
            login(request)
        else:
            signup(request)
    return render(request,"languagelessons/home.html",{})

#dict_keys(['csrfmiddlewaretoken', 'signupusername', 'signupemail', 'signuppass', 'signupconfirmpass'])
def signup(request):
    # Create User_Profile
    form = UserCreationForm(request.POST)
    dir(form.data)
    for field in form:
        print("Field Error {} {}".format(field.name, field.errors))
    if form.is_valid():
        print("Form valid")
        user = form.save()
        user.set_password(user.password)
        user.email = request.POST.get('email')
        user.save()

        messages.success(request, f'Your account has been created. You can log in now!')    
        return login(request)
    return render(request, 'languagelessons/home.html')

#dict_keys(['csrfmiddlewaretoken', 'loginemail', 'loginpass', 'login'])
def login(request):
    user = authenticate(email=request.POST.get('loginusername'), password=request.POST.get('loginpassword'))
    if user is not None:
        login(request, user)
        return redirect('dashboard')
    return render(request, 'languagelessons/home.html', {})

@login_required
def dashboard(request):
    return render(request, 'languagelessons/dashboard.html',{"user_id": request.user.pk})

@login_required
def importlesson(request):
    return render(request,"languagelessons/importlesson.html",{})

# @login_required
def lesson(request):
    return render(request,"languagelessons/lesson.html",{})
