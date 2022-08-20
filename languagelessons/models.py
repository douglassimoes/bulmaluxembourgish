from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
from django.conf.urls.static import static
from django.conf import settings


class Word(models.Model):

    class WordFamiliarity(models.TextChoices):
        new = "1"
        seen = "2"
        familiar = "3"
        known = "4"

    word_name = models.CharField(max_length=200, default="")
    word_meaning = models.CharField(max_length=200, default="")
    word_note = models.CharField(max_length=200, default="")
    word_tag = models.CharField(max_length=200, default="")
    familiarity = models.CharField(max_length=254,choices=WordFamiliarity.choices, default="1")
    last_review = models.DateTimeField()

class Sentence(models.Model):
    words_id = models.ForeignKey(Word, on_delete = models.CASCADE)
    audio = models.URLField(max_length = 200, default="")

class Profile(models.Model):

    class TranslationPreference(models.TextChoices):
        portugese = "Portugese"
        english = "English"
        french = "French"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    words_id = models.ForeignKey(Word, on_delete = models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    translation_preference = models.CharField(max_length=254,choices=TranslationPreference.choices, default="English")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Lesson(models.Model):

    class LessonLevel(models.TextChoices):
        beginner1 = "A1"
        beginner2 = "A2"
        intermediate1 = "B1"
        intermediate2 = "B2"
        advanced1  = "C1"
        advanced2 = "C2"

    title = models.CharField(max_length=200, default="No title")
    page = models.PositiveIntegerField(default=1)
    preview = models.CharField(max_length=1000, default="No preview")
    content_lu = models.CharField(max_length=3000, default="No content")
    content_pt = models.CharField(max_length=3000, default="No content")
    content_en = models.CharField(max_length=3000, default="No content")
    content_fr = models.CharField(max_length=3000, default="No content")
    content_timestamps = models.CharField(max_length=3000, default="No content")
    level = models.CharField(max_length=254,choices=LessonLevel.choices, default="A1")
    audio = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='media',default="lesson01.m4a")


class Course(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    lessons_id = models.ForeignKey(Lesson, on_delete = models.CASCADE)
    title = models.CharField(max_length=200, default="No title")
    familiar_words = models.PositiveIntegerField(default=1)

class ActivityTracker(models.Model):
    user_id = models.ForeignKey(Profile, on_delete = models.CASCADE)
    actual_date = models.DateTimeField(auto_now_add=True)
    listening_time = models.PositiveIntegerField()
    words_read = models.PositiveIntegerField()
    known_words = models.PositiveIntegerField()
    familiar_words = models.PositiveIntegerField()
    words_reviewed = models.PositiveIntegerField()



