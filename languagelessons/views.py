from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from languagelessons import models
from django.core.files.storage import FileSystemStorage
import requests
import unicodedata

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
                preview = request.POST.get('lesson_text')[0:100]
                content = request.POST.get('lesson_text')
                level = "A1"
                audio = file
                lesson = models.Lesson(title=title,page=page,preview=preview,content=content,level=level,audio=audio)
                lesson.save()
    return render(request,"languagelessons/importlesson.html",{})

@login_required
def lessons(request):
    lessonlist = models.Lesson.objects.filter()
    print(lessonlist)
    return render(request,"languagelessons/lessons.html",{"lessons": lessonlist})

@login_required
def lesson(request, pk):
    lesson = models.Lesson.objects.get(pk=pk)
    normalized_content = unicodedata.normalize("NFKD", lesson.content)
    lesson_words = normalized_content.split(" ")
    new_words = []
    for word in lesson_words:
        if "\n" in word:
            many_words = word.split("\n")
            new_words.extend(many_words)
        else:
            new_words.append(word)

    exceptions = ["A)","B)",'D\'J??nni','Fred','1)','2)','3)','4)','5)','6)','7)','8)','1800','18','19','20','21','Kaffi']
    exception_list = []

    lux_terms = ['Z??nn', 'd???Bett', 'hu', 'Hat', 'Fernseh', 'hire', 'hie', 'duscht', 'W??scht', 'w??scht', 'zesumme', 'nach,', "d'J??nni", 'Jo,', 'Hie', 'geet', 'kuckt', 'liest', 'Eise', 'Geet', 'Liest', 'schl??ift', 'um', 'Froen:', 'Hire', 'Duscht', '??sst', 'eise', "d'Bett", 'e', 'hinne', 'Nee,', 'an', 'Kuckt', 'liesen','Kaffi', 'erzielt', 'dee', 'Steet', 'D???Clienten', 'schwa??tzt', 'Dre??nkt', 'fa??nkt', 'eenzege', 'ka', 'schwa??tze', 'fiert', 'd???Clienten', 'sti', 'vum', 'dre??nke', 'Fa??nkt', 'ke??nnt', 'e??nnerschiddleche', 'drop', 'fuere', 'd???Geschicht', 'ville', 'hallwer', 'steet', 'Clienten', '1', 'd???Cienten', 'verschiddene', 'dre??nkt', 'Fiert', 'La??nner', 'd???Aarbecht', 'wann', 'bege??inen', 'fir', 'd???A??ntwerten', 'Misch', 'bereeden','zwou', 'De??mmi', 'Huet', 'huet', 'Fligerticket', 'decide??iert', 'kee', 'am', 'Wochen', 'we??llt', 'We??llt', 'd???Frankra??ich', 'An', 'D???Frankra??ich', 'soll', 'd???Vakanz', 'Schwa??tzt', 'Suen', 'wouhinner', 'Decide??iert', 'Wantervakanz',"d'A??ntwerten", 'schaffe', "D'Enseignante", 'd???Meedche', "d'Meedche", 'Schafft', 'd???Schoul', 'A??nnchen', 'Heescht', "D'A??nnchen", 'vu', "D'Meedche", "D'Meedchen", 'hir', 'Fre??nn', "d'Geschicht", "d'Enseignante", 'Hausaufgaben', 'D???Le??ierpersonal', 'd???Enseignanten', 'le??iere', "d'A??nnchen", 'Jull', "d'Meedchen", 'heescht', 'We??ssenschafte', 'komme', 'Fre??ndin', 'scha??tzt', "d'Schoul","d\'Claire", 'me??cht', 'D???Claire', 'Filmer', 'Me??cht', 'd???Claire', 'spillt', 'D???Claire', 'deet', 'schreift', "D'Claire", 'spille', 'd???Claire', 'Claire', 'Hausaufgabe', 'Spillt', 'Deet']

    google_translation = ['Teeth', 'the bed', 'hu', 'hat', 'television', 'hire', 'he', 'shower', 'wash', 'wash', 'together', 'after, ', "the J??nni",' Yes, ',' He ',' goes ',' looks ',' reads ',' Iron ',' Goes ',' Reads ',' sleeps ',' around ',' Questions: ',' Hire ',' Shower ',' eat ',' our ',' the bed ',' e ',' them ',' no, ',' and ',' look ','read','coffee','tells', 'he', 'stands', 'customers', 'speaks', 'drinks', 'starts', 'single', 'can', 'talk', 'drives', 'd\'Clients ',' stand ',' from ',' drink ',' start ',' come ',' different ',' drop ',' drive ',' history ',' many ',' half ',' stands', 'customers',' 1 ',' customers', 'different', 'drinks',' drives', 'countries',' work ',' when ',' meet ',' for ' , 'the answers', 'mix', 'prepare','two', 'stupid', 'did', 'did', 'plane ticket', 'decided', 'none', 'in', 'weeks', 'want', 'want', 'France' , 'In', 'France', 'should', 'holiday', 'talk', 'money', 'where', 'decided', 'winter holiday', "the answers", 'work', 'the teacher', 'the girl', 'the girl', 'work', 'school', 'little girl', 'mean', 'D\'??nnchen', 'vu'," D'Meedche "," D'Meedchen ", 'hir', 'Friends',' Geschichte ',' d\'Enseignante ',' Homofusen ',' D\'Den Teacher ',' the teachers', 'learn', 'the little girl', 'you', 'the girl', 'mean', 'science', 'come', 'girlfriend', 'appreciate', 'school',"Claire", "does", "Claire", "films", "does", "Claire", "plays", "Claire", "hurts", "writes", " Claire "," play "," Claire "," Claire "," Homework "," Play "," Deet "]

    my_translations = dict(zip(lux_terms, google_translation))
    
    for word in new_words:
        word = word.replace(".","").replace(",","").replace("\r\n","").replace("?","")
        print("\'{}\'".format(word),end='= ')
        if word not in exceptions:
            url = "https://lod.lu/api/lb/entry/"+word.strip().upper()+"1"
            print(url)
            response = requests.get(url)
            if 'entry' in response.json() and 'grammaticalUnits' in response.json()['entry']['microStructures'][0].keys():
                print(response.json()['entry']['microStructures'][0]['grammaticalUnits'][0]['meanings'][0]['targetLanguages']['pt']['parts'][0]['content'])
            else:
                if word in my_translations.keys():
                    print(my_translations[word])
                else:
                    exception_list.append(word)

    print("exceptions: {}, {} words".format(set(exception_list),len(set(exception_list))))
    return render(request,"languagelessons/lesson.html",{"lesson": lesson, "lesson_words": new_words})
