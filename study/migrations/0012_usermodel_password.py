# Generated by Django 3.2.10 on 2023-09-11 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0011_auto_20230911_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='password',
            field=models.CharField(default=1, max_length=12),
        ),
    ]