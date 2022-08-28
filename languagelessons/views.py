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
        response = redirect('lessons')
        response.set_cookie('new_translation_preference',request.POST.get('new_translation_preference'))
        return response
    return render(request,"languagelessons/home.html",{})

# def signup_view(request):
#     if request.method == 'POST':
#         print(request.POST.keys())
#         form = UserCreationForm(request.POST)
#         dir(form.data)
#         for field in form:
#             print("Field Error {} {}".format(field.name, field.errors))
#         if form.is_valid():
#             user = form.save()
#             post = request.POST
#             print("Form valid")
#             messages.success(request, f'Your account has been created. You can log in now!')
#             return redirect('login')    
#     return render(request,"languagelessons/signup.html",{})

# def login_view(request):
#     if request.method == 'POST':
#         print(request.POST.keys())
#         user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#     return render(request,"languagelessons/login.html",{})

# def dashboard(request):
#     return render(request, 'languagelessons/dashboard.html',{"user_id": request.user.pk})

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
                preview = request.POST.get('lesson_text_lu')[0:100]
                content_lu = request.POST.get('lesson_text_lu')
                content_pt = request.POST.get('lesson_text_pt')
                content_en = request.POST.get('lesson_text_en')
                content_fr = request.POST.get('lesson_text_fr')
                level = "A1"
                audio = file
                lesson = models.Lesson(title=title,page=page,preview=preview,content_lu=content_lu,content_pt=content_pt,content_en=content_en,content_fr=content_fr,level=level,audio=audio)
                lesson.save()
    return render(request,"languagelessons/importlesson.html",{})

def timestampeditor(request,pk):
    lesson = models.Lesson.objects.get(pk=pk)
    print(request.COOKIES.get('new_translation_preference'))
    lesson_normalized_content = unicodedata.normalize("NFKD", lesson.content_lu)
    audio_normalized_content = unicodedata.normalize("NFKD", lesson.content_timestamps)
    audio_timestamps = audio_normalized_content.split(";")

    audio_minutes_seconds = []
    timestamp_splits = []
    for timestamp in audio_timestamps:
        audio_minutes_seconds.append(timestamp.split(","))

    delimiter = "."

    lesson_phrases = [x+delimiter for x in lesson_normalized_content.split(delimiter) if x]
    phrase_id = [ i for i in range(len(lesson_phrases))]
    
    lesson_phrases_words = []
    for lesson_phrase_id,lesson_phrase in zip(phrase_id,lesson_phrases):
        lesson_phrase = lesson_phrase.replace(".","").replace(",","").replace("\n"," ").replace("?","")
        lesson_phrases_words.append(lesson_phrase.split(" "))

    amount_list_extension = len(lesson_phrases) - len(audio_timestamps) - 1
    new_audio_minutes_seconds  = [ audio_minutes_seconds.append([["0","0"]])  for i in range(amount_list_extension)]


    lesson_phrases_audio = zip(lesson_phrases,phrase_id,audio_minutes_seconds)

    # print(list(lesson_phrases_audio))

    return render(request,"languagelessons/timestamp_editor.html",{"lesson": lesson, "lesson_phrases": lesson_phrases,"lesson_phrases_audio":lesson_phrases_audio})

def lessons(request):
    lessonlist = models.Lesson.objects.filter()
    print(lessonlist)
    return render(request,"languagelessons/lessons.html",{"lessons": lessonlist})

# def profile(request):
#     if request.method == 'POST':
#         print(request.POST.keys())
#         profile.translation_preference = request.POST.getlist("new_translation_preference")[0]
#         profile.save()
#         return render(request,"languagelessons/profile.html",{"user_data": user, "user_profile": profile})
#     return render(request,"languagelessons/profile.html",{"user_data": user, "user_profile": profile})

def change_translation(request):
    if request.method == 'POST':
        print(request.POST.keys())
        response = redirect('lessons')
        response.set_cookie('new_translation_preference',request.POST.get('new_translation_preference'))
        return response
    return render(request,"languagelessons/change_translation.html", {"translation_preference": request.COOKIES.get('new_translation_preference')})

def lesson(request, pk):
    lesson = models.Lesson.objects.get(pk=pk)
    print(request.COOKIES.get('new_translation_preference'))
    lesson_normalized_content = unicodedata.normalize("NFKD", lesson.content_lu)
    audio_normalized_content = unicodedata.normalize("NFKD", lesson.content_timestamps)

    delimiter = "."

    translation_pt_normalized_content = unicodedata.normalize("NFKD", lesson.content_pt)
    translation_en_normalized_content = unicodedata.normalize("NFKD", lesson.content_en)
    translation_fr_normalized_content = unicodedata.normalize("NFKD", lesson.content_fr)
    translation_pt_phrases = [x+delimiter for x in translation_pt_normalized_content.split(delimiter) if x]
    translation_en_phrases = [x+delimiter for x in translation_en_normalized_content.split(delimiter) if x]
    translation_fr_phrases = [x+delimiter for x in translation_fr_normalized_content.split(delimiter) if x]


    lesson_phrases = [x+delimiter for x in lesson_normalized_content.split(delimiter) if x]
    phrase_id = [ i for i in range(len(lesson_phrases))]
    
    lesson_phrases_words = []
    for lesson_phrase_id,lesson_phrase in zip(phrase_id,lesson_phrases):
        lesson_phrase = lesson_phrase.replace(".","").replace(",","").replace("\n"," ").replace("?","")
        lesson_phrases_words.append(lesson_phrase.split(" "))


    lesson_words = lesson_normalized_content.split(" ")
    audio_timestamps = audio_normalized_content.split(";")
    new_words = []
    for word in lesson_words:
        if "\n" in word:
            many_words = word.split("\n")
            new_words.extend(many_words)
        else:
            new_words.append(word)

    exceptions = ["A)","B)",'D\'Jänni','Fred','1)','2)','3)','4)','5)','6)','7)','8)','1800','18','19','20','21','Kaffi']
    exception_list = []

    translation_dict = { "English":"en", "Portuguese":"pt", "French":"fr"}

    lux_terms = ['Zänn', 'd‘Bett', 'hu', 'Hat', 'Fernseh', 'hire', 'hie', 'duscht', 'Wäscht', 'wäscht', 'zesumme', 'nach,', "d'Jänni", 'Jo,', 'Hie', 'geet', 'kuckt', 'liest', 'Eise', 'Geet', 'Liest', 'schléift', 'um', 'Froen:', 'Hire', 'Duscht', 'ësst', 'eise', "d'Bett", 'e', 'hinne', 'Nee,', 'an', 'Kuckt', 'liesen','Kaffi', 'erzielt', 'dee', 'Steet', 'D’Clienten', 'schwätzt', 'Drénkt', 'fänkt', 'eenzege', 'ka', 'schwätze', 'fiert', 'd’Clienten', 'sti', 'vum', 'drénke', 'Fänkt', 'kënnt', 'ënnerschiddleche', 'drop', 'fuere', 'd’Geschicht', 'ville', 'hallwer', 'steet', 'Clienten', '1', 'd’Cienten', 'verschiddene', 'drénkt', 'Fiert', 'Länner', 'd’Aarbecht', 'wann', 'begéinen', 'fir', 'd’Äntwerten', 'Misch', 'bereeden','zwou', 'Dëmmi', 'Huet', 'huet', 'Fligerticket', 'decidéiert', 'kee', 'am', 'Wochen', 'wëllt', 'Wëllt', 'd’Frankräich', 'An', 'D’Frankräich', 'soll', 'd’Vakanz', 'Schwätzt', 'Suen', 'wouhinner', 'Decidéiert', 'Wantervakanz',"d'Äntwerten", 'schaffe', "D'Enseignante", 'd‘Meedche', "d'Meedche", 'Schafft', 'd’Schoul', 'Ännchen', 'Heescht', "D'Ännchen", 'vu', "D'Meedche", "D'Meedchen", 'hir', 'Frënn', "d'Geschicht", "d'Enseignante", 'Hausaufgaben', 'D‘Léierpersonal', 'd’Enseignanten', 'léiere', "d'Ännchen", 'Jull', "d'Meedchen", 'heescht', 'Wëssenschafte', 'komme', 'Frëndin', 'schätzt', "d'Schoul","d\'Claire", 'mécht', 'D’Claire', 'Filmer', 'Mécht', 'd‘Claire', 'spillt', 'D‘Claire', 'deet', 'schreift', "D'Claire", 'spille', 'd’Claire', 'Claire', 'Hausaufgabe', 'Spillt', 'Deet']

    google_translation = ['Teeth', 'the bed', 'hu', 'hat', 'television', 'hire', 'he', 'shower', 'wash', 'wash', 'together', 'after, ', "the Jänni",' Yes, ',' He ',' goes ',' looks ',' reads ',' Iron ',' Goes ',' Reads ',' sleeps ',' around ',' Questions: ',' Hire ',' Shower ',' eat ',' our ',' the bed ',' e ',' them ',' no, ',' and ',' look ','read','coffee','tells', 'he', 'stands', 'customers', 'speaks', 'drinks', 'starts', 'single', 'can', 'talk', 'drives', 'd\'Clients ',' stand ',' from ',' drink ',' start ',' come ',' different ',' drop ',' drive ',' history ',' many ',' half ',' stands', 'customers',' 1 ',' customers', 'different', 'drinks',' drives', 'countries',' work ',' when ',' meet ',' for ' , 'the answers', 'mix', 'prepare','two', 'stupid', 'did', 'did', 'plane ticket', 'decided', 'none', 'in', 'weeks', 'want', 'want', 'France' , 'In', 'France', 'should', 'holiday', 'talk', 'money', 'where', 'decided', 'winter holiday', "the answers", 'work', 'the teacher', 'the girl', 'the girl', 'work', 'school', 'little girl', 'mean', 'D\'Ännchen', 'vu'," D'Meedche "," D'Meedchen ", 'hir', 'Friends',' Geschichte ',' d\'Enseignante ',' Homofusen ',' D\'Den Teacher ',' the teachers', 'learn', 'the little girl', 'you', 'the girl', 'mean', 'science', 'come', 'girlfriend', 'appreciate', 'school',"Claire", "does", "Claire", "films", "does", "Claire", "plays", "Claire", "hurts", "writes", " Claire "," play "," Claire "," Claire "," Homework "," Play "," Deet "]

    my_translations = dict(zip(lux_terms, google_translation))
    
    for word in new_words:
        word = word.replace(".","").replace(",","").replace("\r\n","").replace("?","")
        # print("\'{}\'".format(word),end='= ')

        if word not in exceptions:
            url = "https://lod.lu/api/lb/entry/"+word.strip().upper()+"1"
            # print(url)
            response = requests.get(url)
            if 'entry' in response.json() and 'grammaticalUnits' in response.json()['entry']['microStructures'][0].keys():
                word_meaning_en = response.json()['entry']['microStructures'][0]['grammaticalUnits'][0]['meanings'][0]['targetLanguages']['en']['parts'][0]['content']
                word_meaning_fr = response.json()['entry']['microStructures'][0]['grammaticalUnits'][0]['meanings'][0]['targetLanguages']['fr']['parts'][0]['content']
                word_meaning_pt = response.json()['entry']['microStructures'][0]['grammaticalUnits'][0]['meanings'][0]['targetLanguages']['pt']['parts'][0]['content']
                word_audio_reference = response.json()['entry']['audioFiles']['aac']
                # if not models.Word.objects.filter(word_name=word).exists():
                new_word = models.Word(word_name=word,word_en_meaning=word_meaning_en,word_fr_meaning=word_meaning_fr,word_pt_meaning=word_meaning_pt,meaning_reference=url,word_audio_reference=word_audio_reference)
                new_word.save()
            else:
                if word in my_translations.keys():
                    empty_str = ""
                    if not models.Word.objects.filter(word_name=word).exists():
                        new_word = models.Word(word_name=word,word_en_meaning=empty_str,word_fr_meaning=empty_str,word_pt_meaning=empty_str,meaning_reference=empty_str,word_audio_reference=empty_str)
                        new_word.save()
                else:
                    exception_list.append(word)

    lesson_phrases_words_meanings = []
    word_meanings = []
    for list_words in lesson_phrases_words:
        for word in list_words:
            if models.Word.objects.filter(word_name=word).exists():
                word_db = models.Word.objects.filter(word_name=word)[0]
                meaning = word_db.word_en_meaning
                reference = word_db.meaning_reference
                word_audio = word_db.word_audio_reference
            else:
                meaning = ""
                reference = ""
                word_audio = ""
            word_meanings.append([word,meaning,reference,word_audio])
        lesson_phrases_words_meanings.append(word_meanings)
        word_meanings = []

    audio_timestamps.extend(audio_timestamps)

    # print(len(lesson_phrases))
    # print(len(phrase_id))
    # print(len(lesson_phrases_words))
    # print(len(translation_pt_phrases))
    # print(len(translation_en_phrases))
    # print(len(translation_fr_phrases))
    # print(len(audio_timestamps))

    print(lesson_phrases_words_meanings)

    lesson_translation = zip(lesson_phrases,phrase_id,lesson_phrases_words_meanings,translation_pt_phrases,translation_en_phrases,translation_fr_phrases,audio_timestamps)
    print("exceptions: {}, {} words".format(set(exception_list),len(set(exception_list))))
    return render(request,"languagelessons/lesson.html",{"lesson": lesson, "lesson_words": new_words, "lesson_phrases": lesson_phrases,"lesson_phrases_words_meanings": lesson_phrases_words_meanings, "lesson_translation":lesson_translation,"translation_preference": request.COOKIES.get('new_translation_preference')})
