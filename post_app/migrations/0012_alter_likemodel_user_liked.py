# Generated by Django 3.2.10 on 2023-12-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0011_likemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likemodel',
            name='user_liked',
            field=models.JSONField(default=''),
        ),
    ]
