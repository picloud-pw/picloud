# Generated by Django 2.0.1 on 2018-01-10 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='complexity',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cloud.Department'),
        ),
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='resources/posts/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='resources/posts/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='course',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='lecturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cloud.Lecturer'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='short_title',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='university',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='resources/u_logo/'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='resources/user_avatars/'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cloud.Program'),
        ),
    ]
