# Generated by Django 3.2.10 on 2023-09-11 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0010_storagedatamodel_money'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storagedatamodel',
            name='money',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='money',
            field=models.CharField(default=0, max_length=20),
        ),
    ]