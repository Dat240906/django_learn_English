# Generated by Django 3.2.10 on 2023-09-13 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0005_auto_20230913_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='notification',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='message',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]