# Generated by Django 2.0.1 on 2018-01-15 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0013_auto_20180115_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='subjects',
        ),
        migrations.AddField(
            model_name='subject',
            name='programs',
            field=models.ManyToManyField(to='cloud.Program'),
        ),
    ]