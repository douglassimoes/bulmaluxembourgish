from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from languagelessons import models
from django.core.files.storage import FileSystemStorage

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
    if request.method == "POST":
        print(request.POST.keys())
        # if the post request has a file under the input name 'audiofile', then save the file.
        print(request.FILES)
        audio_file = request.FILES['audiofile'] if 'audiofile' in request.FILES else None
        if audio_file:
                # save attached file
                print("saving attached file")
                # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                file = fs.save(audio_file.name, audio_file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)
                title = request.POST.get('lesson_title')
                page = 1
                content = request.POST.get('lesson_text')
                level = "A1"
                audio = file
                lesson = models.Lesson(title=title,page=page,content=content,level=level,audio=audio)
                lesson.save()
    return render(request,"languagelessons/importlesson.html",{})

# @login_required
def lessons(request):
    lessonlist = models.Lesson.objects.filter()
    print(lessonlist)
    return render(request,"languagelessons/lessons.html",{"lessons": lessonlist})
