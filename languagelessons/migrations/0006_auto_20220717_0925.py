# Generated by Django 3.2.5 on 2022-07-17 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languagelessons', '0005_lesson_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='preview',
            field=models.CharField(default='No preview', max_length=1000),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=models.CharField(default='No content', max_length=3000),
        ),
    ]