# Generated by Django 3.2.10 on 2023-11-21 13:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0006_alter_postmodel_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='create_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
