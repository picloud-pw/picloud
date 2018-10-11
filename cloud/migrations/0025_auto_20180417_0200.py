# Generated by Django 2.0.1 on 2018-04-16 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0024_auto_20180412_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chair',
            name='validate_status',
        ),
        migrations.RemoveField(
            model_name='department',
            name='validate_status',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='validate_status',
        ),
        migrations.RemoveField(
            model_name='post',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='program',
            name='validate_status',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='validate_status',
        ),
        migrations.RemoveField(
            model_name='university',
            name='validate_status',
        ),
        migrations.AddField(
            model_name='chair',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='department',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='program',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='university',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
    ]
