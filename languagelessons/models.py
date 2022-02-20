from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    words_id = models.ForeignKey(Word, on_delete = models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

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
    content = models.CharField(max_length=1000, default="No content")
    level = models.CharField(max_length=254,choices=LessonLevel.choices, default="A1")


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



