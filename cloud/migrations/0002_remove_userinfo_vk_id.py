# Generated by Django 2.0.2 on 2019-09-16 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='vk_id',
        ),
    ]