# Generated by Django 2.0.1 on 2018-02-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0015_userinfo_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]