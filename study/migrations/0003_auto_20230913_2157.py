# Generated by Django 3.2.10 on 2023-09-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_remove_notificationsmodel_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='message',
            field=models.CharField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='password',
            field=models.CharField(max_length=12),
        ),
    ]
