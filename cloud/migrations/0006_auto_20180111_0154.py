# Generated by Django 2.0.1 on 2018-01-10 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0005_lecturer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttype',
            name='title',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
